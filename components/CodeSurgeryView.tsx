"use client";

import { useState, useEffect } from "react";
import ReactDiffViewer, { DiffMethod } from "react-diff-viewer-continued";
import Mermaid from "@mermaid-js/mermaid-react";
import { Copy, Check, Info, AlertTriangle, Zap } from "lucide-react";

interface CodeSurgeryData {
  diagnosis: string;
  root_cause: string;
  evidence: string;
  original_code_snippet: string;
  fixed_code_snippet: string;
  mermaid_diagram: string;
  severity: "High" | "Medium" | "Low";
  quick_fix: string;
  proper_fix: string;
  prevention: string;
}

interface CodeSurgeryViewProps {
  data: CodeSurgeryData;
}

export default function CodeSurgeryView({ data }: CodeSurgeryViewProps) {
  const [copied, setCopied] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  const handleCopyFix = () => {
    navigator.clipboard.writeText(data.fixed_code_snippet);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const severityColors = {
    High: "text-red-400",
    Medium: "text-yellow-400",
    Low: "text-green-400",
  };

  const hasCode = data.original_code_snippet && data.fixed_code_snippet;

  return (
    <div className="space-y-6">
      {/* Diagnosis & Root Cause */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
        <div className="flex items-start gap-3 mb-3">
          <AlertTriangle className="w-5 h-5 text-neon-purple flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-neon-purple mb-2">
              Diagnosis
            </h3>
            <p className="text-gray-300 text-sm mb-4">{data.diagnosis}</p>
            
            <h4 className="text-md font-semibold text-gray-200 mb-2">
              Root Cause
            </h4>
            <p className="text-gray-400 text-sm">{data.root_cause}</p>
          </div>
          <div className={`text-sm font-semibold ${severityColors[data.severity]}`}>
            Severity: {data.severity}
          </div>
        </div>
      </div>

      {/* Evidence */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
        <h3 className="text-md font-semibold text-gray-200 mb-2 flex items-center gap-2">
          <Info className="w-4 h-4 text-neon-green" />
          Evidence
        </h3>
        <pre className="text-xs text-gray-400 bg-dark-bg p-3 rounded border border-dark-border overflow-x-auto">
          {data.evidence}
        </pre>
      </div>

      {/* Mermaid Diagram */}
      {data.mermaid_diagram && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
          <h3 className="text-md font-semibold text-gray-200 mb-3 flex items-center gap-2">
            <Zap className="w-4 h-4 text-neon-purple" />
            Logic Flow Correction
          </h3>
          <div className="bg-dark-bg rounded border border-dark-border p-4">
            <Mermaid chart={data.mermaid_diagram} />
          </div>
        </div>
      )}

      {/* Code Diff View */}
      {hasCode ? (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-semibold text-neon-purple flex items-center gap-2">
              Code Surgery
            </h3>
            <div className="flex gap-2">
              <button
                onClick={() => setShowExplanation(!showExplanation)}
                className="px-3 py-1.5 text-xs bg-dark-bg border border-dark-border rounded hover:border-neon-purple transition-colors flex items-center gap-1.5"
              >
                <Info className="w-3.5 h-3.5" />
                {showExplanation ? "Hide" : "Explain"}
              </button>
              <button
                onClick={handleCopyFix}
                className="px-3 py-1.5 text-xs bg-neon-purple text-white rounded hover:bg-purple-600 transition-colors flex items-center gap-1.5"
              >
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    Apply Fix
                  </>
                )}
              </button>
            </div>
          </div>

          {showExplanation && (
            <div className="mb-4 p-3 bg-dark-bg border border-dark-border rounded text-sm text-gray-300">
              <p className="mb-2">
                <strong className="text-neon-green">Why this fix:</strong> {data.proper_fix}
              </p>
              <p className="text-xs text-gray-400">{data.prevention}</p>
            </div>
          )}

          <div className="border border-dark-border rounded overflow-hidden">
            <ReactDiffViewer
              oldValue={data.original_code_snippet}
              newValue={data.fixed_code_snippet}
              splitView={true}
              leftTitle="❌ Before (Broken Code)"
              rightTitle="✅ After (Fixed Code)"
              useDarkTheme={true}
              compareMethod={DiffMethod.WORDS}
              styles={{
                variables: {
                  dark: {
                    codeFoldGutterBackground: "#1a1a1a",
                    codeFoldBackground: "#0a0a0a",
                    addedBackground: "#0d4d0d",
                    addedColor: "#00ff41",
                    removedBackground: "#4d0d0d",
                    removedColor: "#ff4444",
                    wordAddedBackground: "#0d4d0d",
                    wordRemovedBackground: "#4d0d0d",
                  },
                },
              }}
            />
          </div>
        </div>
      ) : (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
          <p className="text-gray-400 text-sm">
            No code snippets found in the log. Analysis provided above.
          </p>
        </div>
      )}

      {/* Solutions */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
        <h3 className="text-md font-semibold text-gray-200 mb-3">Solutions</h3>
        <div className="space-y-3">
          <div>
            <span className="text-xs text-neon-green font-semibold">Quick Fix:</span>
            <p className="text-sm text-gray-300 mt-1">{data.quick_fix}</p>
          </div>
          <div>
            <span className="text-xs text-neon-purple font-semibold">Proper Fix:</span>
            <p className="text-sm text-gray-300 mt-1">{data.proper_fix}</p>
          </div>
          <div>
            <span className="text-xs text-gray-400 font-semibold">Prevention:</span>
            <p className="text-sm text-gray-400 mt-1">{data.prevention}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

