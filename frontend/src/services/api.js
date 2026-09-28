const API_BASE = '/api';

export async function fetchStats() {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error('Failed to fetch statistics');
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/categories`);
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function fetchEntries({ category, version, search, letter, page = 1, pageSize = 24 } = {}) {
  const params = new URLSearchParams();
  if (category) params.set('category', category);
  if (version) params.set('version', version);
  if (search) params.set('search', search);
  if (letter) params.set('letter', letter);
  params.set('page', page);
  params.set('page_size', pageSize);

  const res = await fetch(`${API_BASE}/entries?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch entries');
  return res.json();
}

export async function fetchRandomEntry() {
  const res = await fetch(`${API_BASE}/random`);
  if (!res.ok) throw new Error('Failed to fetch random entry');
  return res.json();
}

export async function fetchEntry(slug) {
  const res = await fetch(`${API_BASE}/entries/${slug}`);
  if (!res.ok) throw new Error(`Failed to fetch entry "${slug}"`);
  return res.json();
}

export async function searchEntries(query) {
  if (!query || query.trim().length === 0) return { query: '', results: [] };
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query.trim())}`);
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}

export async function toggleBookmark(slug) {
  const res = await fetch(`${API_BASE}/entries/${slug}/bookmark`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to toggle bookmark');
  return res.json();
}

export async function fetchBookmarks() {
  const res = await fetch(`${API_BASE}/bookmarks`);
  if (!res.ok) throw new Error('Failed to fetch bookmarks');
  return res.json();
}

export async function addCommunityNote(slug, note) {
  const res = await fetch(`${API_BASE}/entries/${slug}/notes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(note)
  });
  if (!res.ok) throw new Error('Failed to add note');
  return res.json();
}

export async function fetchQuiz() {
  const res = await fetch(`${API_BASE}/quiz`);
  if (!res.ok) throw new Error('Failed to fetch quiz');
  return res.json();
}
