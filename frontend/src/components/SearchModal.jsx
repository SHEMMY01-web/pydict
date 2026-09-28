import React, { useState, useEffect, useRef } from 'react';
import { Search, X, CornerDownLeft, Sparkles, BookOpen } from 'lucide-react';
import { searchEntries } from '../services/api';

export default function SearchModal({ isOpen, onClose, onSelectEntry }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery('');
      setResults([]);
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setLoading(false);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await searchEntries(query);
        setResults(data.results || []);
        setSelectedIndex(0);
      } catch (err) {
        console.error('Search error:', err);
      } finally {
        setLoading(false);
      }
    }, 150);

    return () => clearTimeout(timer);
  }, [query]);

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < results.length - 1 ? prev + 1 : prev));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : 0));
    } else if (e.key === 'Enter' && results[selectedIndex]) {
      e.preventDefault();
      onSelectEntry(results[selectedIndex].slug);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="modal-dialog" 
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        <div className="modal-search-box">
          <Search size={20} color="var(--py-blue)" />
          <input
            ref={inputRef}
            type="text"
            className="modal-search-input"
            placeholder="Type a term, syntax, or keyword (e.g. zip, yield, __init__)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          {query && (
            <button 
              className="icon-btn" 
              style={{ width: '28px', height: '28px' }} 
              onClick={() => setQuery('')}
            >
              <X size={16} />
            </button>
          )}
          <span className="shortcut-kbd">ESC</span>
        </div>

        {loading && (
          <div style={{ padding: '1.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Searching Python Lexicon...
          </div>
        )}

        {!loading && query && results.length === 0 && (
          <div style={{ padding: '2.5rem 1.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            <p>No Python terms found matching <strong>"{query}"</strong></p>
            <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>Try searching for built-in functions, dunder methods, or keywords.</p>
          </div>
        )}

        {results.length > 0 && (
          <ul className="search-results-list">
            {results.map((entry, index) => (
              <li
                key={entry.slug}
                className={`search-result-item ${index === selectedIndex ? 'selected' : ''}`}
                onClick={() => {
                  onSelectEntry(entry.slug);
                  onClose();
                }}
                onMouseEnter={() => setSelectedIndex(index)}
              >
                <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, fontSize: '1rem', color: 'var(--text-main)' }}>
                      {entry.term}
                    </span>
                    <span className={`pos-tag pos-${entry.category}`}>
                      {entry.category}
                    </span>
                    {entry.added_in_version && (
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                        v{entry.added_in_version}
                      </span>
                    )}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', maxWidth: '480px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {entry.short_summary}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-dim)' }}>
                  {index === selectedIndex && (
                    <span style={{ display: 'flex', alignItems: 'center', fontSize: '0.75rem', gap: '2px', color: 'var(--py-blue)' }}>
                      Select <CornerDownLeft size={12} />
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}

        {!query && (
          <div style={{ padding: '1rem 1.5rem', background: 'var(--bg-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <span>Search Python keywords, built-ins, and standard library definitions</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              Navigate with <kbd className="shortcut-kbd">↑</kbd> <kbd className="shortcut-kbd">↓</kbd>
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
