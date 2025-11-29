import { NextRequest } from 'next/server';

// Helper endpoint to list available models
export async function GET(req: NextRequest) {
  try {
    const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
    
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "GOOGLE_GENERATIVE_AI_API_KEY not set" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }

    // Try v1 API first (more stable)
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1/models?key=${apiKey}`
    );

    if (!response.ok) {
      // Try v1beta if v1 fails
      const responseBeta = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`
      );
      
      if (!responseBeta.ok) {
        const errorText = await responseBeta.text();
        return new Response(
          JSON.stringify({ 
            error: "Failed to fetch models",
            v1betaError: errorText,
            hint: "Make sure Generative AI API is enabled in Google Cloud Console"
          }),
          { status: 500, headers: { "Content-Type": "application/json" } }
        );
      }
      
      const data = await responseBeta.json();
      return new Response(
        JSON.stringify({ 
          models: data.models || [],
          apiVersion: "v1beta"
        }),
        { headers: { "Content-Type": "application/json" } }
      );
    }

    const data = await response.json();
    return new Response(
      JSON.stringify({ 
        models: data.models || [],
        apiVersion: "v1"
      }),
      { headers: { "Content-Type": "application/json" } }
    );
  } catch (error: any) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}

