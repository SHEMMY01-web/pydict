let pyodideInstance = null;
let pyodideLoadPromise = null;

export async function getPyodide() {
  if (pyodideInstance) {
    return pyodideInstance;
  }

  if (pyodideLoadPromise) {
    return pyodideLoadPromise;
  }

  pyodideLoadPromise = (async () => {
    // Check if pyodide script tag loaded
    if (typeof window.loadPyodide !== 'function') {
      // Dynamic fallback script loader
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }

    console.log('[Pyodide] Initializing WebAssembly Python runtime...');
    pyodideInstance = await window.loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/'
    });
    console.log('[Pyodide] Python runtime ready.');
    return pyodideInstance;
  })();

  return pyodideLoadPromise;
}

export async function runPythonCode(code) {
  const startTime = performance.now();
  try {
    const pyodide = await getPyodide();

    let stdoutBuffer = [];
    let stderrBuffer = [];

    pyodide.setStdout({
      batched: (text) => stdoutBuffer.push(text)
    });
    pyodide.setStderr({
      batched: (text) => stderrBuffer.push(text)
    });

    const result = await pyodide.runPythonAsync(code);
    const duration = Math.round(performance.now() - startTime);

    let output = stdoutBuffer.join('\n');
    if (!output && result !== undefined && result !== null) {
      output = String(result);
    }
    if (!output && stderrBuffer.length === 0) {
      output = '(Code executed successfully with no stdout output)';
    }

    return {
      success: true,
      output: output,
      stderr: stderrBuffer.join('\n'),
      durationMs: duration
    };
  } catch (err) {
    const duration = Math.round(performance.now() - startTime);
    return {
      success: false,
      output: '',
      error: err.message || String(err),
      durationMs: duration
    };
  }
}
