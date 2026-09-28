import React, { useState } from 'react';
import { Play, RotateCcw, Copy, Check, Terminal, Loader2, Sparkles } from 'lucide-react';
import { runPythonCode } from '../services/pyodide';

export default function CodePlayground({ 
  initialCode = '', 
  title = 'Python Interactive Snippet', 
  expectedOutput = null 
}) {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState(expectedOutput ? `Expected Output:\n${expectedOutput}` : '');
  const [isRunning, setIsRunning] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);
  const [isCopied, setIsCopied] = useState(false);
  const [executionTime, setExecutionTime] = useState(null);

  const handleRun = async () => {
    setIsRunning(true);
    setStatusMessage('Running in Pyodide WASM...');
    try {
      const res = await runPythonCode(code);
      setExecutionTime(res.durationMs);

      if (res.success) {
        let finalOut = res.output;
        if (res.stderr) {
          finalOut += `\n[stderr]:\n${res.stderr}`;
        }
        setOutput(finalOut);
        setStatusMessage(`Executed in ${res.durationMs}ms`);
      } else {
        setOutput(`Traceback (most recent call last):\n${res.error}`);
        setStatusMessage(`Error (${res.durationMs}ms)`);
      }
    } catch (err) {
      setOutput(`Execution failed: ${err.message}`);
      setStatusMessage('Failed');
    } finally {
      setIsRunning(false);
    }
  };

  const handleReset = () => {
    setCode(initialCode);
    setOutput(expectedOutput ? `Expected Output:\n${expectedOutput}` : '');
    setStatusMessage(null);
    setExecutionTime(null);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <div className="code-playground">
      {/* Playground Header */}
      <div className="playground-header">
        <div className="playground-title">
          <Terminal size={16} color="#38BDF8" />
          <span>{title}</span>
          <span style={{ fontSize: '0.7rem', color: '#64748B', marginLeft: '6px' }}>
            Pyodide (In-Browser WASM)
          </span>
        </div>

        <div className="playground-actions">
          <button
            className="icon-btn"
            style={{ width: '30px', height: '30px', color: '#CBD5E1' }}
            onClick={handleCopy}
            title="Copy code to clipboard"
          >
            {isCopied ? <Check size={14} color="#10B981" /> : <Copy size={14} />}
          </button>

          <button
            className="icon-btn"
            style={{ width: '30px', height: '30px', color: '#CBD5E1' }}
            onClick={handleReset}
            title="Reset code to original"
          >
            <RotateCcw size={14} />
          </button>

          <button
            className="run-code-btn"
            onClick={handleRun}
            disabled={isRunning}
          >
            {isRunning ? (
              <>
                <Loader2 size={13} className="animate-spin" />
                <span>Running...</span>
              </>
            ) : (
              <>
                <Play size={13} fill="currentColor" />
                <span>Run Code</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Code Editor */}
      <textarea
        className="code-editor-textarea"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={Math.max(4, code.split('\n').length + 1)}
        spellCheck="false"
      />

      {/* Output Console */}
      <div className="output-console">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div className="output-label">Execution Output</div>
          {statusMessage && (
            <span style={{ fontSize: '0.7rem', color: isRunning ? '#38BDF8' : '#A7F3D0' }}>
              {statusMessage}
            </span>
          )}
        </div>
        <div>{output || '(Click "Run Code" to execute this snippet)'}</div>
      </div>
    </div>
  );
}
