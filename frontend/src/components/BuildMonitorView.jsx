import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, CheckCircle, AlertTriangle, Terminal, Download, RefreshCw, Cpu, HardDrive } from 'lucide-react';

export default function BuildMonitorView() {
  const [status, setStatus] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [triggering, setTriggering] = useState(false);
  const logContainerRef = useRef(null);

  // Poll status every 1 second
  useEffect(() => {
    let isMounted = true;

    const fetchStatus = async () => {
      try {
        const res = await fetch('/api/build-status');
        if (res.ok) {
          const data = await res.json();
          if (isMounted) {
            setStatus(data);
            setIsConnected(true);
          }
        } else {
          if (isMounted) setIsConnected(false);
        }
      } catch (err) {
        if (isMounted) setIsConnected(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 1200);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  // Auto-scroll log box
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [status?.recent_logs]);

  const pauseBuild = async () => {
    setTriggering(true);
    try {
      await fetch('/api/build/pause', { method: 'POST' });
    } catch (e) {
      console.error(e);
    } finally {
      setTimeout(() => setTriggering(false), 1000);
    }
  };

  const resumeBuild = async () => {
    setTriggering(true);
    try {
      await fetch('/api/build/resume', { method: 'POST' });
    } catch (e) {
      console.error(e);
    } finally {
      setTimeout(() => setTriggering(false), 1000);
    }
  };

  const getPhaseBadge = (phase) => {
    switch (phase) {
      case 'completed':
        return <span style={{ color: '#16a34a', fontWeight: 'bold' }}>✓ BUILD READY</span>;
      case 'failed':
        return <span style={{ color: '#dc2626', fontWeight: 'bold' }}>✗ FAILED</span>;
      case 'paused':
        return <span style={{ color: '#ea580c', fontWeight: 'bold' }}>⏸ PAUSED (SAFELY SAVED)</span>;
      case 'downloading_ndk':
        return <span style={{ color: '#2563eb', fontWeight: 'bold' }}>DOWNLOADING NDK (PARTIAL RANGE)</span>;
      case 'extracting_ndk':
        return <span style={{ color: '#d97706', fontWeight: 'bold' }}>EXTRACTING TOOLCHAIN</span>;
      case 'assembling_apk':
        return <span style={{ color: '#7c3aed', fontWeight: 'bold' }}>ASSEMBLING GRADLE APK</span>;
      default:
        return <span style={{ color: '#6b7280' }}>STANDBY</span>;
    }
  };

  const downloadedMB = status ? (status.downloaded_bytes / (1024 * 1024)).toFixed(1) : 0;
  const totalMB = status ? (status.total_bytes / (1024 * 1024)).toFixed(1) : 638.3;

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '24px 16px' }}>
      {/* Wiktionary Page Header */}
      <div style={{ borderBottom: '1px solid var(--wiki-border, #a2a9b1)', paddingBottom: '12px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <h1 style={{ fontFamily: 'Linux Libertine, Georgia, serif', fontSize: '28px', margin: '0 0 6px 0', color: 'var(--wiki-text, #202122)' }}>
              PyDict APK Build & Package Center
            </h1>
            <div style={{ fontSize: '13px', color: 'var(--wiki-muted, #54595d)' }}>
              Local Android Compilation Pipeline &bull; Option 2 (On-Device Build)
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {status?.phase === 'downloading_ndk' && (
              <button
                onClick={pauseBuild}
                disabled={triggering}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  backgroundColor: '#ea580c',
                  color: '#ffffff',
                  border: 'none',
                  padding: '6px 12px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '12px',
                  fontWeight: '600'
                }}
              >
                <Pause size={13} />
                <span>Pause Download</span>
              </button>
            )}

            {(status?.phase === 'paused' || status?.phase === 'idle' || status?.phase === 'failed') && (
              <button
                onClick={resumeBuild}
                disabled={triggering}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  backgroundColor: '#2563eb',
                  color: '#ffffff',
                  border: 'none',
                  padding: '6px 12px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '12px',
                  fontWeight: '600'
                }}
              >
                <Play size={13} />
                <span>Resume Download</span>
              </button>
            )}

            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '4px 10px',
              borderRadius: '12px',
              fontSize: '12px',
              backgroundColor: isConnected ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              color: isConnected ? '#16a34a' : '#ef4444',
              border: `1px solid ${isConnected ? '#22c55e' : '#ef4444'}`
            }}>
              <span style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: isConnected ? '#22c55e' : '#ef4444',
                display: 'inline-block',
                animation: isConnected ? 'pulse 2s infinite' : 'none'
              }} />
              {isConnected ? 'Active Connection' : 'Disconnected'}
            </span>
          </div>
        </div>
      </div>

      {/* Overview Table / Wiktionary Infobox */}
      <div style={{ 
        backgroundColor: 'var(--wiki-card-bg, #f8f9fa)', 
        border: '1px solid var(--wiki-border, #c8ccd1)', 
        borderRadius: '4px',
        padding: '16px',
        marginBottom: '20px'
      }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', fontSize: '13px' }}>
          <div>
            <div style={{ color: 'var(--wiki-muted, #54595d)', marginBottom: '4px' }}>Current Phase</div>
            <div>{getPhaseBadge(status?.phase)}</div>
          </div>
          <div>
            <div style={{ color: 'var(--wiki-muted, #54595d)', marginBottom: '4px' }}>Download Progress</div>
            <div style={{ fontWeight: '600' }}>
              {downloadedMB} MB / {totalMB} MB ({status?.percent || 0}%)
            </div>
          </div>
          <div>
            <div style={{ color: 'var(--wiki-muted, #54595d)', marginBottom: '4px' }}>Transfer Speed</div>
            <div style={{ fontWeight: '600' }}>
              {status?.speed_mbps ? `${status.speed_mbps} MB/s` : '0.0 MB/s'}
            </div>
          </div>
          <div>
            <div style={{ color: 'var(--wiki-muted, #54595d)', marginBottom: '4px' }}>Estimated Time (ETA)</div>
            <div style={{ fontWeight: '600' }}>
              {status?.eta_seconds ? `${Math.floor(status.eta_seconds / 60)}m ${status.eta_seconds % 60}s` : 'Calculating...'}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div style={{ marginTop: '16px' }}>
          <div style={{ 
            height: '14px', 
            backgroundColor: 'var(--wiki-border, #eaecf0)', 
            borderRadius: '7px', 
            overflow: 'hidden',
            border: '1px solid var(--wiki-border, #c8ccd1)'
          }}>
            <div style={{ 
              width: `${Math.min(status?.percent || 0, 100)}%`, 
              height: '100%', 
              backgroundColor: status?.phase === 'completed' ? '#16a34a' : '#3366cc',
              transition: 'width 0.4s ease'
            }} />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--wiki-muted, #54595d)', marginTop: '4px' }}>
            <span>Step {status?.step || 0} of {status?.total_steps || 3}: {status?.step_name || 'Standby'}</span>
            <span>{status?.percent || 0}%</span>
          </div>
        </div>
      </div>

      {/* APK Ready Banner */}
      {status?.phase === 'completed' && (
        <div style={{ 
          backgroundColor: '#f0fdf4', 
          border: '1px solid #bbf7d0', 
          borderRadius: '4px', 
          padding: '16px', 
          marginBottom: '20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div>
            <div style={{ color: '#166534', fontWeight: 'bold', fontSize: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <CheckCircle size={20} /> PyDict APK Generated Successfully!
            </div>
            <div style={{ fontSize: '13px', color: '#15803d', marginTop: '4px' }}>
              File: <code style={{ backgroundColor: '#dcfce7', padding: '2px 6px', borderRadius: '3px' }}>app-debug.apk</code> ({status?.apk_size_mb || '28.4'} MB)
            </div>
          </div>
          <a 
            href="/api/download-apk" 
            download="PyDict-debug.apk"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              backgroundColor: '#16a34a',
              color: '#ffffff',
              padding: '8px 16px',
              borderRadius: '4px',
              textDecoration: 'none',
              fontWeight: '600',
              fontSize: '13px'
            }}
          >
            <Download size={16} /> Download APK
          </a>
        </div>
      )}

      {/* Live Terminal Log Stream */}
      <div style={{ 
        backgroundColor: '#1e1e1e', 
        color: '#d4d4d4', 
        borderRadius: '6px', 
        overflow: 'hidden',
        border: '1px solid #333',
        marginBottom: '24px'
      }}>
        <div style={{ 
          backgroundColor: '#2d2d2d', 
          padding: '8px 14px', 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          fontSize: '12px',
          color: '#aaa',
          borderBottom: '1px solid #3d3d3d'
        }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Terminal size={14} color="#36c" /> Live Build Output Log
          </span>
          <span style={{ fontSize: '11px', color: '#888' }}>
            Auto-scrolling &bull; {status?.recent_logs?.length || 0} entries
          </span>
        </div>
        <div 
          ref={logContainerRef}
          style={{ 
            padding: '12px 14px', 
            fontFamily: 'SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace', 
            fontSize: '12px', 
            lineHeight: '1.6',
            height: '240px', 
            overflowY: 'auto',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-all'
          }}
        >
          {status?.recent_logs && status.recent_logs.length > 0 ? (
            status.recent_logs.map((log, idx) => (
              <div key={idx} style={{ 
                color: log.startsWith('ERROR') ? '#f87171' : log.startsWith('SUCCESS') ? '#4ade80' : '#e2e8f0' 
              }}>
                <span style={{ color: '#64748b', marginRight: '8px' }}>&gt;</span>
                {log}
              </div>
            ))
          ) : (
            <div style={{ color: '#71717a' }}>Waiting for output...</div>
          )}
        </div>
      </div>

      {/* Instructions for Installing on Device */}
      <div style={{ borderTop: '1px solid var(--wiki-border, #c8ccd1)', paddingTop: '16px' }}>
        <h3 style={{ fontSize: '15px', margin: '0 0 8px 0', color: 'var(--wiki-text, #202122)' }}>
          Installation Instructions
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--wiki-text, #202122)', lineHeight: '1.5' }}>
          Once the APK finishes compiling, you can install it on your Android phone or emulator with one command:
        </p>
        <pre style={{ 
          backgroundColor: 'var(--wiki-card-bg, #f8f9fa)', 
          border: '1px solid var(--wiki-border, #c8ccd1)', 
          padding: '10px 14px', 
          borderRadius: '4px',
          fontSize: '12px',
          overflowX: 'auto'
        }}>
          adb install -r "/home/olaewevictor01/PY DICT/mobile/android/app/build/outputs/apk/debug/app-debug.apk"
        </pre>
      </div>
    </div>
  );
}
