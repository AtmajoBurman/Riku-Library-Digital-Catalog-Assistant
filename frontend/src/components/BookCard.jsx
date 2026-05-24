import React from 'react';

export default function BookCard({ book }) {
  // Safe helper to format dates in a professional human-readable way
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      // Format as Month DD, YYYY
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit'
      });
    } catch (e) {
      return dateString;
    }
  };

  return (
    <article className="glass-panel book-card" id={`book-card-${book.uid}`}>
      <div className="book-header">
        <h3 className="book-title">{book.title}</h3>
        <span 
          className={`availability-badge ${book.is_available ? 'available' : 'checked-out'}`}
          id={`availability-badge-${book.uid}`}
        >
          <span className="chat-status-dot" style={{ backgroundColor: book.is_available ? '#10b981' : '#f43f5e', boxShadow: `0 0 6px ${book.is_available ? '#10b981' : '#f43f5e'}` }}></span>
          {book.is_available ? 'Available' : 'Checked Out'}
        </span>
      </div>

      <div className="book-author">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        {book.author}
      </div>

      <p className="book-description">{book.description || 'No description provided.'}</p>

      <div className="book-footer">
        <div className="date-box">
          <span className="date-label">Created</span>
          <span className="date-value">{formatDate(book.created_at)}</span>
        </div>
        <div className="date-box">
          <span className="date-label">Updated</span>
          <span className="date-value">{formatDate(book.updated_at)}</span>
        </div>
      </div>
    </article>
  );
}
