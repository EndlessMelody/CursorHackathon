import { google } from '@ai-sdk/google';
import { streamText } from 'ai';

// Tăng giới hạn thời gian xử lý lên 30s (tối đa của Vercel Hobby)
export const maxDuration = 30;

// System Prompt - Code Surgery Mode với JSON output
const SYSTEM_PROMPT = `You are a Senior Site Reliability Engineer specializing in log analysis and code debugging. Your role is to provide precise, technical analysis with visual code fixes.

CRITICAL: You MUST respond with VALID JSON only. No markdown, no explanations outside JSON.

Response Format (STRICT JSON):

{
  "diagnosis": "Brief technical explanation of the bug (1-2 sentences)",
  "root_cause": "Deep technical reason why this error occurs",
  "evidence": "Specific log lines/quotes that prove the diagnosis",
  "original_code_snippet": "Extract the problematic code from the log/context. If no code found, return empty string. Include surrounding context (3-5 lines before/after)",
  "fixed_code_snippet": "The corrected code with the fix applied. Must match the structure of original_code_snippet",
  "mermaid_diagram": "Mermaid flowchart syntax showing the logic flow correction. Example format: flowchart TD\\n  A[Original Flow] -->|Error| B[Problem]\\n  A -->|Fixed| C[Solution]\\n  Use simple, clear flowcharts",
  "severity": "High/Medium/Low",
  "quick_fix": "Immediate workaround (1 sentence)",
  "proper_fix": "Production-ready solution explanation (2-3 sentences)",
  "prevention": "How to avoid this issue in the future (1-2 sentences)"
}

Guidelines:
- Extract code from logs if present (look for file paths, line numbers, code blocks)
- If user provides code snippet, use it as original_code_snippet
- fixed_code_snippet must be complete, compilable code
- mermaid_diagram should be simple flowchart (max 5-7 nodes)
- Be technical and precise. No humor.
- If no code is found in logs, set original_code_snippet and fixed_code_snippet to empty strings
- ALWAYS return valid JSON that can be parsed`;

export async function POST(req: Request) {
  try {
    // 1. Lấy tin nhắn từ Client
    const { messages } = await req.json();

    // 2. Kiểm tra API Key (Debug nhanh)
    if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
      return new Response("Missing GOOGLE_GENERATIVE_AI_API_KEY in .env.local", { status: 500 });
    }

     // 3. Gọi AI - Thử các model theo thứ tự
    // gemini-2.5-flash là model mới nhất và có sẵn
    const modelsToTry = ['gemini-2.5-flash', 'gemini-pro', 'gemini-1.5-pro'];
    let lastError: any = null;
    
    for (const modelName of modelsToTry) {
      try {
        console.log(`Trying model: ${modelName}`);
        const result = await streamText({
          model: google(modelName),
          messages,
          system: SYSTEM_PROMPT,
          temperature: 0.7,
          maxTokens: 2000,
        });
        console.log(`✅ Successfully using model: ${modelName}`);
        return result.toDataStreamResponse();
      } catch (error: any) {
        console.log(`❌ Model ${modelName} failed:`, error.message);
        lastError = error;
        continue;
      }
    }
    
    // Nếu tất cả model đều fail
    const errorMsg = lastError?.message || "All models failed";
    console.error("❌ All models failed. Error:", errorMsg);
    
    return new Response(
      JSON.stringify({ 
        error: "No available Gemini models found",
        details: errorMsg,
        hint: "Visit http://localhost:3000/api/list-models to see available models. Make sure: 1) API key is correct, 2) Billing is set up (even for free tier), 3) Generative AI API is enabled in Google Cloud Console"
      }),
      { 
        status: 500,
        headers: { "Content-Type": "application/json" }
      }
    );

  } catch (error: any) {
    console.error("AI Error:", error);
    
    // Xử lý lỗi trả về cho Client dễ hiểu hơn
    const errorMessage = error.message || "An error occurred with Gemini API";
    
    // Nếu lỗi Quota (429)
    if (errorMessage.includes("429") || errorMessage.includes("quota")) {
      return new Response("Too many requests! Please wait a moment (Google Free Tier limit).", { status: 429 });
    }

    // Nếu lỗi 404 (model not found)
    if (errorMessage.includes("404") || errorMessage.includes("not found")) {
      return new Response(
        JSON.stringify({ 
          error: "Model not available",
          details: errorMessage,
          hint: "Visit http://localhost:3000/api/list-models to check available models. You may need to enable billing or enable the Generative AI API in Google Cloud Console."
        }),
        { 
          status: 500,
          headers: { "Content-Type": "application/json" }
        }
      );
    }

    return new Response(JSON.stringify({ error: errorMessage }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}