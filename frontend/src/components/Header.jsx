import React, { useState } from 'react';
import { Compass, Sparkles, Key, Monitor, CheckCircle, Sliders } from 'lucide-react';

export default function Header({ 
  headed, 
  setHeaded, 
  provider, 
  setProvider, 
  apiKey, 
  setApiKey, 
  apiHealth 
}) {
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [inputKey, setInputKey] = useState(apiKey || '');

  const handleSaveKey = () => {
    setApiKey(inputKey);
    setShowKeyModal(false);
  };

  return (
    <>
      <header className="header-nav">
        <div className="brand-section">
          <div className="brand-logo">
            <Compass size={26} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="brand-title">TestPilot AI</span>
              <span className="brand-badge">PS-03</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              AI-Powered Web Test Case & Bug Script Generator
            </p>
          </div>
        </div>

        <div className="nav-actions">
          {/* Health indicator */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--accent-emerald)', padding: '6px 12px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '20px', border: '1px solid rgba(16, 185, 129, 0.25)' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-emerald)', display: 'inline-block' }} className="pulse"></span>
            Playwright & Engine Ready
          </div>

          {/* Browser Mode Toggle (Headed vs Headless) */}
          <button 
            type="button"
            className={`btn btn-sm ${headed ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setHeaded(!headed)}
            title="Toggle visible browser window during test execution"
          >
            <Monitor size={15} />
            {headed ? 'Headed Window (On)' : 'Headless (Fast)'}
          </button>

          {/* AI Provider Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(255,255,255,0.05)', padding: '4px 8px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <Sparkles size={14} color="var(--accent-cyan)" />
            <select 
              value={provider} 
              onChange={(e) => setProvider(e.target.value)}
              style={{ background: 'transparent', border: 'none', color: '#fff', fontSize: '12px', outline: 'none', cursor: 'pointer' }}
            >
              <option value="hybrid" style={{ background: '#0d121f' }}>Hybrid (Gemini / Heuristic)</option>
              <option value="heuristic" style={{ background: '#0d121f' }}>Smart Heuristic Engine (Offline)</option>
              <option value="gemini" style={{ background: '#0d121f' }}>Google Gemini 2.5</option>
              <option value="openai" style={{ background: '#0d121f' }}>OpenAI GPT-4o</option>
            </select>
          </div>

          {/* API Key Modal Button */}
          <button 
            type="button" 
            className="btn btn-secondary btn-sm"
            onClick={() => setShowKeyModal(true)}
            title="Configure optional API keys"
          >
            <Key size={14} />
            {apiKey ? 'API Key Configured' : 'Configure Key'}
          </button>
        </div>
      </header>

      {/* Key Config Modal */}
      {showKeyModal && (
        <div className="modal-overlay" onClick={() => setShowKeyModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '520px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '18px', fontWeight: 700 }}>LLM Provider API Key</h3>
              <button 
                onClick={() => setShowKeyModal(false)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '20px', cursor: 'pointer' }}
              >
                &times;
              </button>
            </div>
            
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px', lineHeight: 1.5 }}>
              TestPilot AI includes a <b>built-in intelligent heuristic engine</b> that generates comprehensive test cases and executable scripts without an API key. You can also provide a Google Gemini or OpenAI key for LLM-driven test generation.
            </p>

            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px' }}>
                Gemini or OpenAI API Key
              </label>
              <input 
                type="password"
                value={inputKey}
                onChange={(e) => setInputKey(e.target.value)}
                placeholder="AIzaSy... or sk-proj-..."
                className="url-input-field"
                style={{ width: '100%', background: 'rgba(0,0,0,0.5)', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '10px 14px' }}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button className="btn btn-secondary" onClick={() => setShowKeyModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleSaveKey}>Save Key</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
