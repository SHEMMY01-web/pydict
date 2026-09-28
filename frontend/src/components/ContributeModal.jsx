import React, { useState } from 'react';
import { X, Send, MessageSquare, Lightbulb, AlertTriangle, Globe } from 'lucide-react';
import { addCommunityNote } from '../services/api';

export default function ContributeModal({ isOpen, onClose, entrySlug, entryTerm, onNoteAdded }) {
  const [author, setAuthor] = useState('');
  const [category, setCategory] = useState('tip');
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;

    setSubmitting(true);
    setError(null);
    try {
      await addCommunityNote(entrySlug, {
        author: author.trim() || 'Anonymous Pythonista',
        category,
        content: content.trim()
      });
      setContent('');
      setAuthor('');
      onNoteAdded?.();
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to submit contribution.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '520px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1.25rem 1.5rem', borderBottom: '1px solid var(--border-light)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <MessageSquare size={18} color="var(--py-blue)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
              Contribute Tip or Note for <code style={{ color: 'var(--py-blue)' }}>{entryTerm}</code>
            </h3>
          </div>
          <button className="icon-btn" onClick={onClose} style={{ width: '28px', height: '28px' }}>
            <X size={16} />
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {error && (
            <div style={{ background: 'var(--rose-soft)', color: 'var(--rose)', padding: '0.6rem 0.85rem', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem' }}>
              {error}
            </div>
          )}

          <div>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '0.35rem' }}>
              Your Name or Handle (Optional)
            </label>
            <input
              type="text"
              className="search-input"
              style={{ paddingLeft: '0.85rem' }}
              placeholder="e.g. Guido, Ada, or Anonymous"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '0.35rem' }}>
              Contribution Type
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem' }}>
              {[
                { id: 'tip', label: 'Pro-Tip', icon: Lightbulb },
                { id: 'analogy', label: 'Analogy', icon: Globe },
                { id: 'warning', label: 'Gotcha', icon: AlertTriangle }
              ].map((item) => {
                const Icon = item.icon;
                const active = category === item.id;
                return (
                  <button
                    type="button"
                    key={item.id}
                    onClick={() => setCategory(item.id)}
                    className="nav-btn"
                    style={{
                      justifyContent: 'center',
                      background: active ? 'var(--py-blue-soft)' : 'var(--bg-subtle)',
                      color: active ? 'var(--py-blue)' : 'var(--text-secondary)',
                      borderColor: active ? 'var(--py-blue)' : 'transparent',
                      fontWeight: active ? 700 : 500
                    }}
                  >
                    <Icon size={14} />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '0.35rem' }}>
              Your Note / Idiom / Example / Explanation
            </label>
            <textarea
              className="code-editor-textarea"
              style={{
                background: 'var(--bg-subtle)',
                color: 'var(--text-main)',
                border: '1px solid var(--border-light)',
                borderRadius: 'var(--radius-md)',
                minHeight: '110px'
              }}
              placeholder="Share an analogy, performance tip, cross-language comparison, or common bug..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem' }}>
            <button type="button" className="nav-btn" onClick={onClose}>
              Cancel
            </button>
            <button
              type="submit"
              className="run-code-btn"
              style={{ background: 'linear-gradient(135deg, #2563EB, #1D4ED8)' }}
              disabled={submitting || !content.trim()}
            >
              <Send size={14} />
              <span>{submitting ? 'Publishing...' : 'Publish Note'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
