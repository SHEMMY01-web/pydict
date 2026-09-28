import React from 'react';
import { Search, Moon, Sun, BookOpen, ExternalLink, Terminal, Dices } from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  onOpenSearch,
  onRandomEntry,
  isRandomLoading = false,
  theme,
  toggleTheme,
  bookmarkCount = 0
}) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        {/* Brand */}
        <div 
          className="brand-logo" 
          onClick={() => setActiveTab('lexicon')}
          style={{ cursor: 'pointer' }}
          role="button"
          tabIndex={0}
        >
          <span className="brand-icon-text">Py</span>
          <div className="brand-text-group">
            <span className="brand-title">PyKtionary</span>
            <span className="brand-badge">The free Python dictionary</span>
          </div>
        </div>

        {/* Global Search */}
        <button 
          className="search-trigger-btn"
          onClick={onOpenSearch}
          title="Search entries (Ctrl+K or /)"
        >
          <Search size={15} />
          <span className="search-placeholder-text">Search PyKtionary</span>
          <span className="shortcut-kbd">⌘K</span>
        </button>

        {/* Navigation Tabs */}
        <div className="nav-actions">
          <button
            className={`nav-btn ${activeTab === 'lexicon' ? 'active' : ''}`}
            onClick={() => setActiveTab('lexicon')}
          >
            <span>Read</span>
          </button>

          <button
            className={`nav-btn ${activeTab === 'playground' ? 'active' : ''}`}
            onClick={() => setActiveTab('playground')}
            style={{ display: 'inline-flex', alignItems: 'center', gap: '5px' }}
            title="Interactive Python WebAssembly Playground"
          >
            <Terminal size={14} />
            <span>Playground</span>
          </button>

          <button
            className={`nav-btn ${activeTab === 'quiz' ? 'active' : ''}`}
            onClick={() => setActiveTab('quiz')}
          >
            <span>Quiz</span>
          </button>

          <button
            className={`nav-btn ${activeTab === 'bookmarks' ? 'active' : ''}`}
            onClick={() => setActiveTab('bookmarks')}
          >
            <span>Saved {bookmarkCount > 0 && `(${bookmarkCount})`}</span>
          </button>

          {/* Random Entry Button */}
          {onRandomEntry && (
            <button
              className="nav-btn"
              onClick={onRandomEntry}
              disabled={isRandomLoading}
              title="Jump to a random Python dictionary entry (Special:Random)"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}
            >
              <Dices size={14} className={isRandomLoading ? 'animate-spin' : ''} />
              <span>Random</span>
            </button>
          )}

          {/* Interactive API Docs Link */}
          <a
            href="/docs"
            target="_blank"
            rel="noreferrer"
            className="nav-btn docs-btn"
            title="Open Interactive FastAPI Swagger Docs"
            style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', textDecoration: 'none' }}
          >
            <BookOpen size={14} />
            <span>Docs</span>
            <ExternalLink size={10} style={{ opacity: 0.6 }} />
          </a>

          <button
            className="icon-btn"
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Light mode' : 'Dark mode'}
            aria-label="Toggle Theme"
          >
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        </div>
      </div>
    </header>
  );
}
