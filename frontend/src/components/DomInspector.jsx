import React, { useState } from 'react';
import { Layers, Image as ImageIcon, ExternalLink, Search, Check, Maximize2 } from 'lucide-react';

export default function DomInspector({ inspection }) {
  const [search, setSearch] = useState('');
  const [showScreenshotModal, setShowScreenshotModal] = useState(false);

  if (!inspection) return null;

  const elements = inspection.elements || [];
  const filteredElements = elements.filter(el => {
    const q = search.toLowerCase();
    return (
      (el.selector || '').toLowerCase().includes(q) ||
      (el.tag || '').toLowerCase().includes(q) ||
      (el.text || '').toLowerCase().includes(q) ||
      (el.placeholder || '').toLowerCase().includes(q) ||
      (el.name || '').toLowerCase().includes(q)
    );
  });

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={20} color="var(--accent-cyan)" />
            <h2 style={{ fontSize: '18px', fontWeight: 700 }}>DOM Inspection Matrix</h2>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Target: <b>{inspection.title}</b> ({inspection.url})
          </p>
        </div>

        {inspection.screenshot_url && (
          <button 
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => setShowScreenshotModal(true)}
          >
            <ImageIcon size={14} />
            View Screenshot
          </button>
        )}
      </div>

      {/* Metrics Row */}
      <div className="metrics-row" style={{ marginBottom: '20px' }}>
        <div className="metric-card">
          <span className="label">Total Discovered</span>
          <span className="value" style={{ color: 'var(--accent-cyan)' }}>{inspection.elements_count}</span>
        </div>
        <div className="metric-card">
          <span className="label">Input Fields</span>
          <span className="value" style={{ color: 'var(--accent-emerald)' }}>{inspection.inputs_count}</span>
        </div>
        <div className="metric-card">
          <span className="label">Action Buttons</span>
          <span className="value" style={{ color: 'var(--accent-purple)' }}>{inspection.buttons_count}</span>
        </div>
        <div className="metric-card">
          <span className="label">Active Forms</span>
          <span className="value" style={{ color: 'var(--accent-amber)' }}>{inspection.forms_count}</span>
        </div>
      </div>

      {/* Search Input */}
      <div style={{ marginBottom: '14px', position: 'relative' }}>
        <input
          type="text"
          className="url-input-field"
          style={{ width: '100%', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '8px 12px' }}
          placeholder="Filter harvested elements by tag, selector, name, or text..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Elements Table */}
      <div style={{ maxHeight: '280px', overflowY: 'auto', border: '1px solid var(--border-subtle)', borderRadius: '8px' }}>
        <table className="test-steps-table">
          <thead>
            <tr>
              <th style={{ width: '80px' }}>Tag</th>
              <th>Resilient Selector</th>
              <th>Attributes & Value</th>
              <th style={{ width: '90px' }}>Visibility</th>
            </tr>
          </thead>
          <tbody>
            {filteredElements.map((el, idx) => (
              <tr key={idx}>
                <td>
                  <span style={{ 
                    fontSize: '11px', 
                    fontWeight: 700, 
                    padding: '2px 6px', 
                    borderRadius: '4px', 
                    background: el.tag === 'button' ? 'rgba(168,85,247,0.2)' : 'rgba(56,189,248,0.2)',
                    color: el.tag === 'button' ? '#c084fc' : '#38bdf8'
                  }}>
                    {el.tag.toUpperCase()}
                  </span>
                </td>
                <td>
                  <code>{el.selector}</code>
                  {el.test_id && (
                    <span style={{ fontSize: '11px', color: 'var(--accent-emerald)', marginLeft: '6px' }}>
                      [test-id: {el.test_id}]
                    </span>
                  )}
                </td>
                <td style={{ fontSize: '12px' }}>
                  {el.text && <div>Text: <i>"{el.text}"</i></div>}
                  {el.placeholder && <div>Placeholder: <i>"{el.placeholder}"</i></div>}
                  {el.name && <div>Name: <code>{el.name}</code></div>}
                </td>
                <td>
                  {el.is_visible ? (
                    <span style={{ color: 'var(--accent-emerald)', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Check size={12} /> Visible
                    </span>
                  ) : (
                    <span style={{ color: 'var(--text-subtle)', fontSize: '12px' }}>Hidden</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Screenshot Lightbox Modal */}
      {showScreenshotModal && inspection.screenshot_url && (
        <div className="modal-overlay" onClick={() => setShowScreenshotModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '960px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: 700 }}>Harvested Target Page Snapshot</h3>
              <button 
                onClick={() => setShowScreenshotModal(false)}
                style={{ background: 'transparent', border: 'none', color: '#fff', fontSize: '20px', cursor: 'pointer' }}
              >
                &times;
              </button>
            </div>
            <div style={{ borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
              <img 
                src={inspection.screenshot_url} 
                alt="Target Page Screenshot" 
                style={{ width: '100%', height: 'auto', display: 'block' }} 
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
