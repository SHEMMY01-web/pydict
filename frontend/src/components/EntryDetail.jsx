import React, { useState, useEffect } from 'react';
import { 
  ArrowLeft, Volume2, Bookmark, ExternalLink, Play, RotateCcw, 
  Copy, Check, Plus, MessageSquare, Share2, Printer, BookOpen 
} from 'lucide-react';
import { fetchEntry, toggleBookmark } from '../services/api';
import { runPythonCode } from '../services/pyodide';
import ContributeModal from './ContributeModal';

function renderFormattedDefinition(text) {
  if (!text) return null;
  const parts = text.split(/(`[^`]+`)/g);
  return parts.map((part, index) => {
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
      return (
        <code key={index} className="wiki-inline-code">
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
}

function CleanCodeExample({ title, initialCode }) {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleRun = async () => {
    setRunning(true);
    try {
      const res = await runPythonCode(code);
      setOutput(res.output || res.error || '(Executed with no output)');
    } catch (err) {
      setOutput(`Error: ${err.message}`);
    } finally {
      setRunning(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="example-box">
      <div className="example-header">
        <span>{title}</span>
        <div style={{ display: 'flex', gap: '0.4rem' }}>
          <button className="wiki-action-btn" onClick={handleCopy}>
            {copied ? <Check size={12} /> : <Copy size={12} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
          <button className="wiki-action-btn" onClick={handleRun} disabled={running}>
            <Play size={12} />
            <span>{running ? 'Running...' : 'Run'}</span>
          </button>
        </div>
      </div>
      <textarea
        className="code-textarea"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={Math.max(3, code.split('\n').length)}
        spellCheck="false"
      />
      {output && <div className="console-output">{output}</div>}
    </div>
  );
}

export default function EntryDetail({ slug, onBack, onSelectEntry, onToggleBookmark }) {
  const [entry, setEntry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchEntry(slug);
      setEntry(data);
      setIsBookmarked(data.is_bookmarked);
    } catch (err) {
      setError(err.message || 'Failed to load entry');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [slug]);

  const handleToggleBookmark = async () => {
    try {
      const res = await toggleBookmark(slug);
      setIsBookmarked(res.is_bookmarked);
      onToggleBookmark?.(slug);
    } catch (err) {
      console.error(err);
    }
  };

  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const speakTerm = () => {
    if (!entry) return;
    setIsPlayingAudio(true);

    const cleanTerm = entry.term.replace(/__/g, ' double underscore ').replace(/\(\)/g, '').trim();
    const audioUrl = `/api/tts?term=${encodeURIComponent(cleanTerm)}`;
    const audio = new Audio(audioUrl);

    audio.onended = () => setIsPlayingAudio(false);
    audio.onerror = () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(cleanTerm);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.onend = () => setIsPlayingAudio(false);
        utterance.onerror = () => setIsPlayingAudio(false);
        window.speechSynthesis.speak(utterance);
      } else {
        setIsPlayingAudio(false);
      }
    };

    audio.play().catch(() => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(cleanTerm);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.onend = () => setIsPlayingAudio(false);
        utterance.onerror = () => setIsPlayingAudio(false);
        window.speechSynthesis.speak(utterance);
      } else {
        setIsPlayingAudio(false);
      }
    });
  };

  if (loading) {
    return (
      <div style={{ padding: '4rem 1rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        Loading entry...
      </div>
    );
  }

  if (error || !entry) {
    return (
      <div className="wiktionary-view" style={{ textAlign: 'center', padding: '3rem' }}>
        <h2>Entry Not Found</h2>
        <p style={{ margin: '1rem 0', color: 'var(--text-secondary)' }}>{error}</p>
        <button className="wiki-action-btn" onClick={onBack}>
          <ArrowLeft size={14} /> Back to Lexicon
        </button>
      </div>
    );
  }

  const hasSenses = entry.senses && entry.senses.length > 0;
  const hasTimeline = entry.version_timeline && entry.version_timeline.length > 0;
  const hasGotchas = entry.gotchas && entry.gotchas.length > 0;
  const hasTrans = entry.cross_language && Object.keys(entry.cross_language).length > 0;

  return (
    <article className="wiktionary-view">
      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
        <button className="wiki-action-btn" onClick={onBack}>
          <ArrowLeft size={14} /> <span>All entries</span>
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <button 
            className="wiki-action-btn" 
            onClick={() => {
              navigator.clipboard.writeText(window.location.href);
              setCopiedLink(true);
              setTimeout(() => setCopiedLink(false), 2000);
            }}
            title="Copy entry link to clipboard"
          >
            {copiedLink ? <Check size={13} color="#10B981" /> : <Share2 size={13} />}
            <span>{copiedLink ? 'Copied' : 'Share'}</span>
          </button>

          <button 
            className="wiki-action-btn" 
            onClick={() => window.print()}
            title="Print or export as PDF"
          >
            <Printer size={13} />
            <span>Print</span>
          </button>

          <button className="wiki-action-btn" onClick={handleToggleBookmark}>
            <Bookmark size={13} fill={isBookmarked ? 'currentColor' : 'none'} />
            <span>{isBookmarked ? 'Saved' : 'Save'}</span>
          </button>
        </div>
      </div>

      {/* Headword Section */}
      <header className="entry-headword-wrap">
        <div style={{ display: 'flex', alignItems: 'baseline' }}>
          <h1 className="entry-headword">{entry.term}</h1>
          {entry.pronunciation && (
            <div className="pronunciation-line">
              <span className="ipa-text">{entry.pronunciation}</span>
              <button 
                className={`tts-speaker-btn ${isPlayingAudio ? 'playing' : ''}`}
                onClick={speakTerm} 
                title={isPlayingAudio ? "Playing pronunciation audio..." : "Listen to pronunciation"}
                aria-label="Listen to pronunciation"
                disabled={isPlayingAudio}
              >
                <Volume2 size={16} className={isPlayingAudio ? "audio-pulse" : ""} />
              </button>
            </div>
          )}
        </div>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Python Language Reference
        </span>
      </header>

      {/* Table of Contents Box */}
      <nav className="toc-box" aria-label="Contents">
        <div className="toc-title">Contents</div>
        <ul className="toc-list">
          <li className="toc-item"><a href="#etymology">1 Etymology & History</a></li>
          {entry.pronunciation && <li className="toc-item"><a href="#pronunciation">2 Pronunciation</a></li>}
          <li className="toc-item"><a href="#definition">3 {entry.part_of_speech}</a></li>
          {hasGotchas && <li className="toc-item"><a href="#usage-notes">4 Usage notes</a></li>}
          {hasTrans && <li className="toc-item"><a href="#translations">5 Translations</a></li>}
          {hasTimeline && <li className="toc-item"><a href="#history">6 Evolutionary History</a></li>}
          <li className="toc-item"><a href="#notes">7 Discussion</a></li>
        </ul>
      </nav>

      {/* 1. Etymology */}
      <section id="etymology">
        <h2 className="wiki-heading">Etymology & Origin</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          {entry.added_in_version && <>First introduced in <strong>Python {entry.added_in_version}</strong>. </>}
          {entry.pep_reference && (
            <>
              Specified in{' '}
              <a href={entry.pep_url || 'https://peps.python.org/'} target="_blank" rel="noopener noreferrer">
                {entry.pep_reference} <ExternalLink size={11} style={{ display: 'inline' }} />
              </a>
              .{' '}
            </>
          )}
          {entry.deprecated_in_version && (
            <span style={{ color: '#c5221f' }}>Deprecated in Python {entry.deprecated_in_version}.</span>
          )}
        </p>
      </section>

      {/* 2. Pronunciation */}
      {entry.pronunciation && (
        <section id="pronunciation">
          <h2 className="wiki-heading">Pronunciation</h2>
          <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)' }}>
            <li>IPA: <span style={{ fontFamily: 'var(--font-mono)' }}>{entry.pronunciation}</span></li>
          </ul>
        </section>
      )}

      {/* 3. Definition & Senses */}
      <section id="definition">
        <h2 className="wiki-heading">{entry.part_of_speech}</h2>

        {entry.signature && (
          <div className="signature-box">
            <code>{entry.signature}</code>
          </div>
        )}

        {/* If Polysemic (Multiple Senses) */}
        {hasSenses ? (
          <ol className="definition-list">
            {entry.senses.map((sense) => (
              <li key={sense.sense_number} className="definition-item">
                <span className="definition-context">({sense.part_of_speech.toLowerCase()})</span>
                <strong>{sense.summary}</strong>
                {sense.signature && (
                  <div>
                    <code style={{ fontSize: '0.8rem', background: 'var(--bg-subtle)', padding: '2px 5px' }}>
                      {sense.signature}
                    </code>
                  </div>
                )}
                {sense.description && (
                  <p style={{ margin: '0.25rem 0', color: 'var(--text-secondary)' }}>
                    {sense.description}
                  </p>
                )}
                {sense.example_code && (
                  <CleanCodeExample 
                    title={`Example (Sense ${sense.sense_number})`} 
                    initialCode={sense.example_code} 
                  />
                )}
              </li>
            ))}
          </ol>
        ) : (
          /* Single Sense Standard Definition */
          <ol className="definition-list">
            <li className="definition-item">
              <span className="definition-context">(programming)</span>
              <span>{entry.short_summary}</span>
              {entry.full_description && (
                <div style={{ marginTop: '0.5rem', color: 'var(--text-secondary)', whiteSpace: 'pre-line' }}>
                  {entry.full_description}
                </div>
              )}
            </li>
          </ol>
        )}

        {/* Simple Definition / Plain-Language Breakdown */}
        {entry.simple_definition && (
          <div className="simple-definition-box">
            <div className="simple-definition-header">
              <span className="simple-def-icon">
                <BookOpen size={14} />
              </span>
              <span className="simple-def-label">In Plain English</span>
              <span className="simple-def-badge">Summary</span>
            </div>
            <p className="simple-definition-text">
              {renderFormattedDefinition(entry.simple_definition)}
            </p>
          </div>
        )}

        {/* Parameters */}
        {entry.parameters && entry.parameters.length > 0 && (
          <div style={{ marginTop: '1rem' }}>
            <h3 className="wiki-subheading">Parameters</h3>
            <table className="wiki-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Type</th>
                  <th>Default</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {entry.parameters.map((p, idx) => (
                  <tr key={idx}>
                    <td><code>{p.name}</code></td>
                    <td><code>{p.type || 'Any'}</code></td>
                    <td><code>{p.default || 'None'}</code></td>
                    <td>{p.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Return Type */}
        {entry.returns && (
          <p style={{ marginTop: '0.75rem', fontSize: '0.9rem' }}>
            <strong>Returns:</strong> <code>{entry.returns.type}</code> — {entry.returns.description}
          </p>
        )}

        {/* Standard Runnable Examples (if single sense) */}
        {!hasSenses && entry.examples && entry.examples.length > 0 && (
          <div style={{ marginTop: '1rem' }}>
            <h3 className="wiki-subheading">Examples</h3>
            {entry.examples.map((ex, idx) => (
              <CleanCodeExample
                key={idx}
                title={ex.title}
                initialCode={ex.code}
              />
            ))}
          </div>
        )}
      </section>

      {/* 4. Usage Notes (Gotchas) */}
      {hasGotchas && (
        <section id="usage-notes">
          <h2 className="wiki-heading">Usage notes</h2>
          <div className="usage-notes-box">
            <ul className="usage-notes-list">
              {entry.gotchas.map((g, idx) => (
                <li key={idx}>{g}</li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* 5. Translations (Cross-Language Equivalents) */}
      {hasTrans && (
        <section id="translations">
          <h2 className="wiki-heading">Translations & Equivalents</h2>
          <div className="translations-box">
            <div className="translations-header">Cross-language analogies</div>
            <div className="translations-grid">
              {Object.entries(entry.cross_language).map(([lang, eq]) => (
                <div key={lang} className="trans-item">
                  <span className="trans-lang">{lang}:</span>
                  <span className="trans-val">{eq}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 6. Evolutionary Version History */}
      {hasTimeline && (
        <section id="history">
          <h2 className="wiki-heading">History</h2>
          <table className="timeline-table">
            <thead>
              <tr>
                <th style={{ width: '110px' }}>Version</th>
                <th>Change</th>
              </tr>
            </thead>
            <tbody>
              {entry.version_timeline.map((event, idx) => (
                <tr key={idx}>
                  <td><strong>Python {event.version}</strong></td>
                  <td>
                    <strong>{event.title}</strong>
                    {event.pep && <span> ({event.pep})</span>}: {event.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {/* 7. Community Notes / Discussion */}
      <section id="notes">
        <div className="wiki-heading">
          <span>Notes & Discussion ({entry.notes?.length || 0})</span>
          <button className="wiki-action-btn" onClick={() => setIsModalOpen(true)}>
            <Plus size={12} /> Add note
          </button>
        </div>

        {entry.notes && entry.notes.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginTop: '0.5rem' }}>
            {entry.notes.map((n) => (
              <div key={n.id} style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-subtle)', padding: '0.6rem 0.85rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
                  <strong>{n.author}</strong>
                  <span>{n.category}</span>
                </div>
                <div style={{ fontSize: '0.875rem' }}>{n.content}</div>
              </div>
            ))}
          </div>
        ) : (
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
            No community notes recorded yet.
          </p>
        )}
      </section>

      {/* See also */}
      {entry.related_entries && entry.related_entries.length > 0 && (
        <section id="see-also">
          <h2 className="wiki-heading">See also</h2>
          <ul style={{ paddingLeft: '1.25rem' }}>
            {entry.related_entries.map((rel) => (
              <li key={rel.slug} style={{ margin: '0.2rem 0' }}>
                <a 
                  href={`#${rel.slug}`} 
                  onClick={(e) => {
                    e.preventDefault();
                    onSelectEntry(rel.slug);
                  }}
                >
                  {rel.term}
                </a>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}> — {rel.short_summary}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Contribute Modal */}
      <ContributeModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        entrySlug={entry.slug}
        entryTerm={entry.term}
        onNoteAdded={loadData}
      />
    </article>
  );
}
