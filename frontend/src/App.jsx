import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import EntryCard from './components/EntryCard';
import EntryDetail from './components/EntryDetail';
import WordOfTheDay from './components/WordOfTheDay';
import SearchModal from './components/SearchModal';
import QuizMode from './components/QuizMode';
import PlaygroundView from './components/PlaygroundView';
import AlphabetBar from './components/AlphabetBar';
import { 
  fetchStats, fetchEntries, fetchCategories, 
  fetchBookmarks, toggleBookmark, fetchRandomEntry
} from './services/api';
import { Search, Bookmark, ChevronLeft, ChevronRight, BookOpen, Layers } from 'lucide-react';

export default function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('pyktionary_theme') || 'dark';
  });

  const [activeTab, setActiveTab] = useState('lexicon'); // 'lexicon', 'playground', 'quiz', 'bookmarks'
  const [selectedSlug, setSelectedSlug] = useState(null);
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  const [stats, setStats] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedVersion, setSelectedVersion] = useState(null);
  const [selectedLetter, setSelectedLetter] = useState(null);
  const [searchInput, setSearchInput] = useState('');

  const [entries, setEntries] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [loadingEntries, setLoadingEntries] = useState(false);
  const [isRandomLoading, setIsRandomLoading] = useState(false);

  const [bookmarks, setBookmarks] = useState([]);
  const [bookmarkedSlugs, setBookmarkedSlugs] = useState(new Set());

  // Apply theme to document root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('pyktionary_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  // Keyboard shortcut listener (Cmd+K or / to search, R for random)
  useEffect(() => {
    const handleKeyDown = (e) => {
      const isInputFocused = ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName);

      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(true);
      } else if (e.key === '/' && !isInputFocused) {
        e.preventDefault();
        setIsSearchOpen(true);
      } else if (e.key.toLowerCase() === 'r' && !isInputFocused && !e.ctrlKey && !e.metaKey) {
        handleRandomEntry();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Load Initial Metadata
  useEffect(() => {
    loadAppMetadata();
    loadBookmarks();
  }, []);

  const loadAppMetadata = async () => {
    try {
      const [statsData, catData] = await Promise.all([
        fetchStats(),
        fetchCategories()
      ]);
      setStats(statsData);
      setCategories(catData);
    } catch (err) {
      console.error('Failed to load stats/categories:', err);
    }
  };

  const loadBookmarks = async () => {
    try {
      const data = await fetchBookmarks();
      setBookmarks(data);
      setBookmarkedSlugs(new Set(data.map((b) => b.slug)));
    } catch (err) {
      console.error('Failed to load bookmarks:', err);
    }
  };

  // Fetch entries on filter/page change
  useEffect(() => {
    if (activeTab !== 'lexicon' || selectedSlug) return;

    const loadEntries = async () => {
      setLoadingEntries(true);
      try {
        const res = await fetchEntries({
          category: selectedCategory,
          version: selectedVersion,
          search: searchInput,
          letter: selectedLetter,
          page,
          pageSize: 21
        });
        setEntries(res.items);
        setTotalPages(res.total_pages);
        setTotalCount(res.total);
      } catch (err) {
        console.error('Failed to load entries:', err);
      } finally {
        setLoadingEntries(false);
      }
    };

    const timer = setTimeout(loadEntries, searchInput ? 200 : 0);
    return () => clearTimeout(timer);
  }, [activeTab, selectedSlug, selectedCategory, selectedVersion, selectedLetter, searchInput, page]);

  const handleSelectEntry = (slug) => {
    setSelectedSlug(slug);
    setActiveTab('lexicon');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleBackToLexicon = () => {
    setSelectedSlug(null);
  };

  const handleRandomEntry = async () => {
    setIsRandomLoading(true);
    try {
      const res = await fetchRandomEntry();
      if (res && res.slug) {
        handleSelectEntry(res.slug);
      }
    } catch (err) {
      console.error('Failed to fetch random entry:', err);
    } finally {
      setIsRandomLoading(false);
    }
  };

  const handleToggleBookmark = async (slug) => {
    try {
      const res = await toggleBookmark(slug);
      setBookmarkedSlugs((prev) => {
        const next = new Set(prev);
        if (res.is_bookmarked) {
          next.add(slug);
        } else {
          next.delete(slug);
        }
        return next;
      });
      loadBookmarks();
    } catch (err) {
      console.error(err);
    }
  };

  // Reload bookmarks whenever switching to bookmarks tab
  useEffect(() => {
    if (activeTab === 'bookmarks') {
      loadBookmarks();
    }
  }, [activeTab]);

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setActiveTab(tab);
          setSelectedSlug(null);
        }}
        onOpenSearch={() => setIsSearchOpen(true)}
        onRandomEntry={handleRandomEntry}
        isRandomLoading={isRandomLoading}
        theme={theme}
        toggleTheme={toggleTheme}
        bookmarkCount={bookmarks.length}
      />

      {/* Main Layout */}
      <main className={`main-layout ${selectedSlug || activeTab !== 'lexicon' ? 'single-column' : ''}`}>
        {/* Sidebar (shown on Lexicon browse mode) */}
        {!selectedSlug && activeTab === 'lexicon' && (
          <Sidebar
            categories={categories}
            selectedCategory={selectedCategory}
            onSelectCategory={(cat) => {
              setSelectedCategory(cat);
              setSelectedLetter(null);
              setPage(1);
            }}
            versions={stats?.versions || []}
            selectedVersion={selectedVersion}
            onSelectVersion={(ver) => {
              setSelectedVersion(ver);
              setSelectedLetter(null);
              setPage(1);
            }}
            totalEntries={stats?.total_entries || totalCount}
          />
        )}

        {/* Content Area */}
        <section className="content-area">
          {/* Detailed Entry Wiktionary View */}
          {selectedSlug ? (
            <EntryDetail
              slug={selectedSlug}
              onBack={handleBackToLexicon}
              onSelectEntry={handleSelectEntry}
              onToggleBookmark={handleToggleBookmark}
            />
          ) : activeTab === 'playground' ? (
            /* Interactive In-Browser Python WASM Playground */
            <PlaygroundView onSelectEntry={handleSelectEntry} />
          ) : activeTab === 'quiz' ? (
            /* Interactive Quiz Mode */
            <QuizMode onSelectEntry={handleSelectEntry} />
          ) : activeTab === 'bookmarks' ? (
            /* Saved Bookmarks View */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-light)', paddingBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Bookmark size={18} color="var(--py-gold)" fill="var(--py-gold)" />
                  <h2 style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-serif)' }}>
                    Saved definitions ({bookmarks.length})
                  </h2>
                </div>
                <button className="wiki-action-btn" onClick={() => setActiveTab('lexicon')}>
                  All entries
                </button>
              </div>

              {bookmarks.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '5rem 1rem', color: 'var(--text-muted)' }}>
                  <p style={{ fontSize: '1.1rem' }}>No saved definitions</p>
                  <p style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    Click the bookmark icon on any definition to save it.
                  </p>
                </div>
              ) : (
                <div className="entries-grid">
                  {bookmarks.map((entry) => (
                    <EntryCard
                      key={entry.slug}
                      entry={entry}
                      onSelect={handleSelectEntry}
                      onToggleBookmark={handleToggleBookmark}
                      isBookmarked={true}
                    />
                  ))}
                </div>
              )}
            </div>
          ) : (
            /* Standard Lexicon Catalog View */
            <>
              {/* Word of the Day Banner */}
              {!selectedCategory && !selectedVersion && !selectedLetter && !searchInput && page === 1 && (
                <WordOfTheDay
                  entry={stats?.word_of_the_day}
                  onSelect={handleSelectEntry}
                />
              )}

              {/* Mobile Horizontal Category Bar */}
              <div className="mobile-category-bar">
                <button
                  className={`mobile-cat-chip ${!selectedCategory ? 'active' : ''}`}
                  onClick={() => { setSelectedCategory(null); setSelectedLetter(null); setPage(1); }}
                >
                  All ({stats?.total_entries || totalCount})
                </button>
                {categories.map((cat) => (
                  <button
                    key={cat.category}
                    className={`mobile-cat-chip ${selectedCategory === cat.category ? 'active' : ''}`}
                    onClick={() => { setSelectedCategory(cat.category); setSelectedLetter(null); setPage(1); }}
                  >
                    {cat.label} ({cat.count})
                  </button>
                ))}
              </div>

              {/* A-Z Alphabetical Navigation Bar */}
              <AlphabetBar
                selectedLetter={selectedLetter}
                onSelectLetter={(letter) => {
                  setSelectedLetter(letter);
                  setPage(1);
                }}
              />

              {/* Filtering Controls Bar */}
              <div className="controls-bar">
                <div className="search-input-wrap">
                  <Search size={16} className="search-icon-inside" />
                  <input
                    type="text"
                    className="search-input"
                    placeholder="Filter by name, summary or tag..."
                    value={searchInput}
                    onChange={(e) => {
                      setSearchInput(e.target.value);
                      setSelectedLetter(null);
                      setPage(1);
                    }}
                  />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  {selectedLetter && (
                    <span className="wiki-pill" style={{ marginRight: '4px' }}>
                      Letter: {selectedLetter.toUpperCase()}
                    </span>
                  )}
                  <span>Showing {entries.length} of {totalCount} definitions</span>
                </div>
              </div>

              {/* Entries Grid */}
              {loadingEntries ? (
                <div style={{ textAlign: 'center', padding: '5rem 1rem', color: 'var(--text-muted)' }}>
                  Loading Python definitions...
                </div>
              ) : entries.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '5rem 1rem', color: 'var(--text-muted)', background: 'var(--bg-surface)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-light)' }}>
                  <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>No definitions found matching your criteria</p>
                  <p style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>Try clearing filters or search for another term.</p>
                  <button 
                    className="wiki-action-btn" 
                    style={{ marginTop: '1rem' }}
                    onClick={() => {
                      setSelectedCategory(null);
                      setSelectedVersion(null);
                      setSelectedLetter(null);
                      setSearchInput('');
                      setPage(1);
                    }}
                  >
                    Reset all filters
                  </button>
                </div>
              ) : (
                <div className="entries-grid">
                  {entries.map((entry) => (
                    <EntryCard
                      key={entry.slug}
                      entry={entry}
                      onSelect={handleSelectEntry}
                      onToggleBookmark={handleToggleBookmark}
                      isBookmarked={bookmarkedSlugs.has(entry.slug)}
                    />
                  ))}
                </div>
              )}

              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="pagination-bar">
                  <button
                    className="nav-btn"
                    disabled={page <= 1}
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                  >
                    <ChevronLeft size={16} />
                    <span>Previous</span>
                  </button>

                  <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    Page {page} of {totalPages}
                  </span>

                  <button
                    className="nav-btn"
                    disabled={page >= totalPages}
                    onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  >
                    <span>Next</span>
                    <ChevronRight size={16} />
                  </button>
                </div>
              )}
            </>
          )}
        </section>
      </main>

      {/* Quick Search Modal */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSelectEntry={handleSelectEntry}
      />
    </div>
  );
}
