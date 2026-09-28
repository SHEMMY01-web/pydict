import React from 'react';
import { Bookmark, Sparkles, ArrowRight } from 'lucide-react';

export default function EntryCard({ entry, onSelect, onToggleBookmark, isBookmarked }) {
  const handleBookmarkClick = (e) => {
    e.stopPropagation();
    onToggleBookmark(entry.slug);
  };

  return (
    <div 
      className="entry-card" 
      onClick={() => onSelect(entry.slug)}
      tabIndex={0}
      role="button"
    >
      <div className="entry-card-header">
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', flexWrap: 'wrap' }}>
          <span className="entry-card-term">{entry.term}</span>
          {entry.pronunciation && (
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {entry.pronunciation.split(' ')[0]}
            </span>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {entry.sense_count > 1 && (
            <span className="mini-tag" style={{ background: 'var(--purple-soft)', color: 'var(--purple)', fontWeight: 700, fontSize: '0.7rem' }}>
              {entry.sense_count} Senses
            </span>
          )}
          <span className={`pos-tag pos-${entry.category}`}>
            {entry.category}
          </span>
          <button
            className="icon-btn"
            style={{ width: '28px', height: '28px' }}
            onClick={handleBookmarkClick}
            title={isBookmarked ? "Remove bookmark" : "Save to bookmarks"}
          >
            <Bookmark 
              size={14} 
              fill={isBookmarked ? "var(--py-gold)" : "none"} 
              color={isBookmarked ? "var(--py-gold)" : "var(--text-muted)"} 
            />
          </button>
        </div>
      </div>

      {entry.signature && (
        <div className="entry-card-signature" title={entry.signature}>
          {entry.signature}
        </div>
      )}

      <p className="entry-card-summary">
        {entry.short_summary}
      </p>

      <div className="entry-card-footer">
        <div className="tags-row">
          {entry.added_in_version && (
            <span className="mini-tag" style={{ color: 'var(--py-blue)', fontWeight: 600 }}>
              Python {entry.added_in_version}
            </span>
          )}
          {entry.tags?.slice(0, 2).map((t) => (
            <span key={t} className="mini-tag">
              #{t}
            </span>
          ))}
        </div>

        <span style={{ display: 'flex', alignItems: 'center', gap: '2px', color: 'var(--py-blue)', fontWeight: 600 }}>
          View <ArrowRight size={12} />
        </span>
      </div>
    </div>
  );
}
