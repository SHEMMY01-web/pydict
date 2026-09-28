import React from 'react';

const ALPHABET = [
  'All', '#',
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
  'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
  'W', 'X', 'Y', 'Z'
];

export default function AlphabetBar({ selectedLetter, onSelectLetter }) {
  return (
    <nav className="az-bar-container" aria-label="Alphabetical index">
      <span className="az-bar-label">Index:</span>
      {ALPHABET.map((item) => {
        const isAll = item === 'All';
        const isActive = isAll ? !selectedLetter : selectedLetter?.toUpperCase() === item;

        return (
          <button
            key={item}
            type="button"
            className={`az-bar-btn ${isAll ? 'all-btn' : ''} ${isActive ? 'active' : ''}`}
            onClick={() => onSelectLetter(isAll ? null : item.toLowerCase())}
            title={isAll ? 'Show all entries' : `Browse terms starting with "${item}"`}
            aria-pressed={isActive}
          >
            {item}
          </button>
        );
      })}
    </nav>
  );
}
