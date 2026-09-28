import React from 'react';

export default function WordOfTheDay({ entry, onSelect }) {
  if (!entry) return null;

  return (
    <div className="wotd-box">
      <div>
        <div className="wotd-title-label">Python word of the day</div>
        <div>
          <a 
            href={`#${entry.slug}`}
            className="wotd-term-link"
            onClick={(e) => {
              e.preventDefault();
              onSelect(entry.slug);
            }}
          >
            {entry.term}
          </a>
          <span style={{ marginLeft: '0.6rem', color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.85rem' }}>
            ({entry.part_of_speech.toLowerCase()})
          </span>
          {entry.pronunciation && (
            <span style={{ marginLeft: '0.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              {entry.pronunciation}
            </span>
          )}
        </div>
        <p style={{ marginTop: '0.35rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          {entry.short_summary}
        </p>
      </div>

      <button 
        className="wiki-action-btn"
        onClick={() => onSelect(entry.slug)}
      >
        Read entry →
      </button>
    </div>
  );
}
