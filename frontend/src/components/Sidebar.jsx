import React from 'react';

export default function Sidebar({
  categories = [],
  selectedCategory,
  onSelectCategory,
  versions = [],
  selectedVersion,
  onSelectVersion,
  totalEntries = 0
}) {
  return (
    <aside className="sidebar">
      {/* Categories / Navigation */}
      <div className="sidebar-card">
        <div className="sidebar-title">Categories</div>
        <ul className="category-nav-list">
          <li
            className={`category-nav-item ${!selectedCategory ? 'active' : ''}`}
            onClick={() => onSelectCategory(null)}
          >
            <span>All entries</span>
            <span className="category-pill-count">{totalEntries}</span>
          </li>

          {categories.map((cat) => (
            <li
              key={cat.category}
              className={`category-nav-item ${selectedCategory === cat.category ? 'active' : ''}`}
              onClick={() => onSelectCategory(cat.category)}
            >
              <span>{cat.label}</span>
              <span className="category-pill-count">{cat.count}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Version Filter */}
      <div className="sidebar-card">
        <div className="sidebar-title">Version</div>
        <select
          className="version-select"
          value={selectedVersion || ''}
          onChange={(e) => onSelectVersion(e.target.value || null)}
        >
          <option value="">All versions</option>
          {versions.map((ver) => (
            <option key={ver} value={ver}>
              Python {ver}+
            </option>
          ))}
        </select>
      </div>
    </aside>
  );
}
