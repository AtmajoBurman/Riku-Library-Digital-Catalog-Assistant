import React, { useState, useEffect, useMemo } from 'react';
import Dashboard from './components/Dashboard';
import SearchBar from './components/SearchBar';
import BookCard from './components/BookCard';
import ChatWidget from './components/ChatWidget';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Search State
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('title');

  // Chat State
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isChatTyping, setIsChatTyping] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    {
      id: 'welcome',
      sender: 'riku',
      text: "Hello! I am Riku, your library assistant. How can I help you today? Ask me about book availability, library rules, or search queries!",
      timestamp: new Date()
    }
  ]);


  // Fetch catalog books
  useEffect(() => {
    async function fetchBooks() {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE}/books/`);
        if (!res.ok) {
          throw new Error(`Failed to fetch catalog. HTTP status: ${res.status}`);
        }
        const data = await res.json();
        setBooks(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching catalog data:', err);
        setError('Could not connect to the library database server. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    }
    fetchBooks();
  }, []);

  // Client-side filtering & search processing
  const filteredBooks = useMemo(() => {
    if (!searchQuery) return books;
    
    return books.filter((book) => {
      if (searchType === 'title') {
        return book.title.toLowerCase().includes(searchQuery.toLowerCase());
      }
      if (searchType === 'author') {
        return book.author.toLowerCase().includes(searchQuery.toLowerCase());
      }
      
      // Date Search: match YYYY-MM-DD
      if (searchType === 'created_at' || searchType === 'updated_at') {
        const isoString = book[searchType];
        if (!isoString) return false;
        
        // Extract the YYYY-MM-DD part from backend datetime string
        const itemDatePart = isoString.split('T')[0];
        return itemDatePart === searchQuery; // searchQuery is YYYY-MM-DD from datepicker
      }
      
      return true;
    });
  }, [books, searchQuery, searchType]);

  // Calculations for Stats
  const totalBooks = books.length;
  const availableBooks = books.filter(b => b.is_available).length;

  // Handle messaging with Riku
  const handleSendMessage = async (text) => {
    // Add user message to state
    const userMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: text,
      timestamp: new Date()
    };
    
    setChatMessages((prev) => [...prev, userMessage]);
    setIsChatTyping(true);

    try {
      const res = await fetch(`${API_BASE}/chatbot`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text })
      });

      if (!res.ok) {
        throw new Error('API server error');
      }

      const data = await res.json();
      
      const rikuMessage = {
        id: `riku-${Date.now()}`,
        sender: 'riku',
        text: data.response || "No response received.",
        timestamp: new Date()
      };
      
      setChatMessages((prev) => [...prev, rikuMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = {
        id: `riku-err-${Date.now()}`,
        sender: 'riku',
        text: "I'm having trouble connecting to the network right now. Please try again in a few seconds.",
        timestamp: new Date()
      };
      setChatMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsChatTyping(false);
    }
  };

  const handleClearFilters = () => {
    setSearchQuery('');
  };

  return (
    <div className="app-container">
      {/* 1. Statistics Dashboard */}
      <Dashboard 
        totalBooks={totalBooks} 
        availableBooks={availableBooks} 
        onAdminClick={() => { window.location.href = `${API_BASE}/login`; }}
      />

      {/* 2. Advanced Search Panel */}
      <SearchBar 
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        searchType={searchType}
        setSearchType={setSearchType}
        onClear={handleClearFilters}
      />

      {/* 3. Catalog Section */}
      <main className="books-section" aria-label="Library Book Catalog">
        <h2 className="books-section-title">
          Book Catalog
          <span className="book-count-badge" id="catalog-count-badge">
            {filteredBooks.length} {filteredBooks.length === 1 ? 'book' : 'books'}
          </span>
        </h2>

        {loading ? (
          // Sleek glassmorphic skeleton loader
          <div className="books-grid" id="loading-skeletons">
            {[1, 2, 3].map(n => (
              <div key={n} className="glass-panel book-card skeleton" style={{ minHeight: '260px', opacity: 0.5, animation: 'pulse 1.5s infinite alternate' }}>
                <div style={{ height: '24px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '4px', marginBottom: '1rem', width: '70%' }}></div>
                <div style={{ height: '14px', backgroundColor: 'rgba(255,255,255,0.04)', borderRadius: '4px', marginBottom: '1.5rem', width: '40%' }}></div>
                <div style={{ height: '80px', backgroundColor: 'rgba(255,255,255,0.03)', borderRadius: '6px', marginBottom: '1.5rem' }}></div>
                <div style={{ display: 'flex', gap: '1rem', marginTop: 'auto' }}>
                  <div style={{ height: '20px', backgroundColor: 'rgba(255,255,255,0.04)', borderRadius: '4px', flex: 1 }}></div>
                  <div style={{ height: '20px', backgroundColor: 'rgba(255,255,255,0.04)', borderRadius: '4px', flex: 1 }}></div>
                </div>
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', border: '1px solid rgba(244, 63, 94, 0.3)', background: 'rgba(244, 63, 94, 0.05)' }}>
            <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '48px', height: '48px', color: '#f43f5e', marginBottom: '1rem' }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p style={{ color: 'var(--color-text-primary)', fontWeight: '600' }}>{error}</p>
            <button className="btn btn-secondary" style={{ marginTop: '1rem' }} onClick={() => window.location.reload()}>Retry Connection</button>
          </div>
        ) : filteredBooks.length === 0 ? (
          <div className="glass-panel empty-books-box" id="empty-results-view">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <h3>No books found</h3>
            <p>We couldn't find any catalog matches. Try adjusting your search query or selector parameters.</p>
          </div>
        ) : (
          <div className="books-grid" id="catalog-books-list">
            {filteredBooks.map((book) => (
              <BookCard key={book.uid} book={book} />
            ))}
          </div>
        )}
      </main>

      {/* 4. Collapsible Chat Widget with Riku */}
      <ChatWidget 
        isOpen={isChatOpen}
        setIsOpen={setIsChatOpen}
        messages={chatMessages}
        onSendMessage={handleSendMessage}
        isTyping={isChatTyping}
      />

    </div>
  );
}
