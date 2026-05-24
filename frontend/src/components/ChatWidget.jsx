import React, { useState, useEffect, useRef } from 'react';

export default function ChatWidget({ isOpen, setIsOpen, messages, onSendMessage, isTyping }) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  // Automatically scroll chat container to the bottom when messages list or typing state changes
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  return (
    <div className="chat-trigger-container">
      {/* 1. Collapsed State: Show Trigger Button & Pill */}
      {!isOpen && (
        <>
          <div className="chat-label-pill">Chat with library assistant Riku</div>
          <button 
            type="button" 
            className="chat-trigger-bubble" 
            onClick={() => setIsOpen(true)}
            id="chat-open-button"
            aria-label="Open Chat with Riku"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/>
            </svg>
          </button>
        </>
      )}

      {/* 2. Expanded State: Show Chat Drawer */}
      {isOpen && (
        <div className="glass-panel chat-drawer" id="chat-drawer-container">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-profile">
              <div className="chat-avatar" aria-hidden="true">🤖</div>
              <div className="chat-header-info">
                <h4>Riku</h4>
                <span><span className="chat-status-dot"></span> Library Assistant</span>
              </div>
            </div>
            <button 
              type="button" 
              className="chat-close-btn" 
              onClick={() => setIsOpen(false)}
              id="chat-close-button"
              aria-label="Close Chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages History */}
          <div className="chat-messages-container" id="chat-messages-list">
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`chat-bubble ${msg.sender}`}
              >
                {msg.text}
                <span className="chat-time">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            ))}

            {/* Riku is Typing state */}
            {isTyping && (
              <div className="chat-typing-bubble" id="riku-typing-indicator" aria-label="Riku is typing">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <form className="chat-input-area" onSubmit={handleSubmit}>
            <input
              type="text"
              className="chat-input-field"
              placeholder="Ask Riku about books or availability..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={isTyping}
              id="chat-message-input"
              maxLength={500}
              autoComplete="off"
            />
            <button 
              type="submit" 
              className="chat-send-btn"
              disabled={!inputText.trim() || isTyping}
              id="chat-send-button"
              aria-label="Send Message"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
