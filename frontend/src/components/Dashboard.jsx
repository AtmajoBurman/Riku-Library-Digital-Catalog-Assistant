import React from 'react';

export default function Dashboard({ totalBooks, availableBooks, onAdminClick }) {
  return (
    <div className="dashboard-container" style={{ marginBottom: '2.5rem' }}>
      {/* Top Header Row */}
      <header className="app-header">
        <div className="brand-section">
          <div className="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 21c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-18C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 9h2v6h-2v-6zm0-4h2v2h-2V7z"/>
            </svg>
          </div>
          <div>
            <h1 className="app-title" id="main-heading">Riku Library</h1>
            <p style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', marginTop: '0.1rem' }}>
              Digital Catalog & Assistant
            </p>
          </div>
        </div>
        
        <button 
          className="btn btn-admin" 
          onClick={onAdminClick}
          id="btn-admin-portal"
          aria-label="Admin Portal"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Admin Portal
        </button>
      </header>

      {/* Stats Counter Section */}
      <section className="stats-grid" aria-label="Library Overview Statistics">
        <div className="glass-panel stat-card" id="stat-total-books">
          <div className="stat-info">
            <h3>Total Catalog</h3>
            <div className="stat-number">{totalBooks}</div>
          </div>
          <div className="stat-icon-box total" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
        </div>

        <div className="glass-panel stat-card" id="stat-available-books">
          <div className="stat-info">
            <h3>Available Now</h3>
            <div className="stat-number">{availableBooks}</div>
          </div>
          <div className="stat-icon-box available" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </section>
    </div>
  );
}
