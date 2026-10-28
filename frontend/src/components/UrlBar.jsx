import React, { useState } from 'react';
import { Globe, Search, Play, Sparkles, SlidersHorizontal, Loader2 } from 'lucide-react';

export default function UrlBar({ 
  url, 
  setUrl, 
  onInspectAndGenerate, 
  onInspectOnly, 
  loading, 
  presets = [] 
}) {
  const [showOptions, setShowOptions] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');

  const handlePresetSelect = (presetUrl) => {
    setUrl(presetUrl);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!url.trim() || loading) return;
    onInspectAndGenerate(url, customPrompt);
  };

  return (
    <div className="glass-panel hero-box">
      <div className="hero-header">
        <div>
          <h1>Autonomous Web Test Automation</h1>
          <p className="hero-subtitle">
            Enter any target web URL or pick a demo scenario. Playwright will inspect the DOM, generate test suites, and execute live tests to catch and reproduce bugs.
          </p>
        </div>
      </div>

      {/* Preset Pills */}
      <div className="presets-container">
        <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-subtle)', marginRight: '4px' }}>
          Quick Demo Presets:
        </span>
        {presets.map((preset) => (
          <button
            key={preset.id}
            type="button"
            className={`preset-pill ${url === preset.url ? 'active' : ''}`}
            onClick={() => handlePresetSelect(preset.url)}
            title={preset.description}
          >
            {preset.recommended && <span style={{ color: 'var(--accent-amber)' }}>★</span>}
            {preset.name}
          </button>
        ))}
      </div>

      {/* Main Input Bar */}
      <form onSubmit={handleFormSubmit}>
        <div className="url-input-group">
          <div style={{ display: 'flex', alignItems: 'center', paddingLeft: '10px', color: 'var(--accent-cyan)' }}>
            <Globe size={18} />
          </div>
          <input
            type="text"
            className="url-input-field"
            placeholder="https://example.com or http://127.0.0.1:8000/demo/shop"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={loading}
          />
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => setShowOptions(!showOptions)}
            title="Add custom testing instructions"
          >
            <SlidersHorizontal size={14} />
            Options
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => onInspectOnly(url)}
            disabled={loading || !url.trim()}
          >
            <Search size={16} />
            Inspect DOM
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !url.trim()}
          >
            {loading ? (
              <>
                <Loader2 size={16} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
                Analyzing Page...
              </>
            ) : (
              <>
                <Sparkles size={16} />
                Generate Test Suite
              </>
            )}
          </button>
        </div>

        {/* Custom Instructions Accordion */}
        {showOptions && (
          <div style={{ marginTop: '12px', padding: '14px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px' }}>
              Custom Test Matrix Directive (Optional)
            </label>
            <input
              type="text"
              className="url-input-field"
              style={{ width: '100%', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-subtle)', borderRadius: '6px' }}
              placeholder="e.g. Focus on cart quantity edge cases and coupon code crash probes"
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
            />
          </div>
        )}
      </form>
    </div>
  );
}
