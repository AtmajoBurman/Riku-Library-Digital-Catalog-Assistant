import React from 'react';

export default function SearchBar({ 
  searchQuery, 
  setSearchQuery, 
  searchType, 
  setSearchType,
  onClear
}) {
  const handleTypeChange = (e) => {
    setSearchType(e.target.value);
    setSearchQuery(''); // Reset query on search type swap
  };

  const isDateSearch = searchType === 'created_at' || searchType === 'updated_at';

  return (
    <div className="glass-panel search-panel">
      <div className="search-grid">
        {/* Search Input Box */}
        <div className="search-input-wrapper">
          {!isDateSearch ? (
            <>
              {/* Text Search */}
              <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                className="search-input"
                placeholder={searchType === 'author' ? 'Search by author name...' : 'Search by book title...'}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                id="search-text-input"
              />
            </>
          ) : (
            <div className="date-filter-group" style={{ width: '100%' }}>
              <label htmlFor="search-date-input">Select Date:</label>
              <input
                type="date"
                id="search-date-input"
                className="date-picker-input"
                style={{ width: '100%', flexGrow: 1 }}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.preventDefault()}
                onClick={(e) => e.target.showPicker && e.target.showPicker()}
              />
            </div>
          )}
        </div>

        {/* Dropdown Criteria */}
        <div>
          <select 
            className="select-filter" 
            value={searchType} 
            onChange={handleTypeChange}
            id="search-type-select"
            aria-label="Search Criteria"
          >
            <option value="title">Search by Name</option>
            <option value="author">Search by Author</option>
            <option value="created_at">Search by Date Created</option>
            <option value="updated_at">Search by Date Updated</option>
          </select>
        </div>
      </div>

      {/* Date picker helper label and clear button */}
      <div className="date-filter-row">
        <span style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)' }}>
          {isDateSearch 
            ? `Showing books matching the selected ${searchType === 'created_at' ? 'creation' : 'modification'} date.`
            : `Filtering catalog by ${searchType}.`}
        </span>
        
        {searchQuery && (
          <button 
            type="button" 
            className="clear-btn" 
            onClick={onClear}
            id="btn-clear-search"
          >
            Clear Filters
          </button>
        )}
      </div>
    </div>
  );
}
