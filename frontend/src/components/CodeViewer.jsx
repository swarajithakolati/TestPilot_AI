import React, { useState } from 'react';
import { Code2, Copy, Download, Check, Terminal } from 'lucide-react';

export default function CodeViewer({ testSuite }) {
  const [activeTab, setActiveTab] = useState('python');
  const [copied, setCopied] = useState(false);

  if (!testSuite) return null;

  const currentCode = activeTab === 'python' 
    ? testSuite.playwright_python_code 
    : testSuite.playwright_ts_code;

  const filename = activeTab === 'python' ? 'test_playwright.py' : 'test_playwright.spec.ts';

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([currentCode], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Code2 size={20} color="var(--accent-cyan)" />
          <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Automation Script Generator Hub</h2>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button 
            type="button" 
            className="btn btn-secondary btn-sm"
            onClick={handleCopy}
            title="Copy script to clipboard"
          >
            {copied ? <Check size={14} color="var(--accent-emerald)" /> : <Copy size={14} />}
            {copied ? 'Copied!' : 'Copy Code'}
          </button>
          <button 
            type="button" 
            className="btn btn-primary btn-sm"
            onClick={handleDownload}
            title="Download executable script file"
          >
            <Download size={14} />
            Download {filename}
          </button>
        </div>
      </div>

      <div className="tabs-bar" style={{ padding: 0, marginBottom: '12px' }}>
        <button
          type="button"
          className={`tab-btn ${activeTab === 'python' ? 'active' : ''}`}
          onClick={() => setActiveTab('python')}
        >
          <Terminal size={15} />
          Playwright (Python)
        </button>
        <button
          type="button"
          className={`tab-btn ${activeTab === 'typescript' ? 'active' : ''}`}
          onClick={() => setActiveTab('typescript')}
        >
          <Terminal size={15} />
          Playwright (TypeScript / Node)
        </button>
      </div>

      <div className="code-container">
        <div className="code-header">
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--text-muted)' }}>
            {filename}
          </span>
          <span style={{ fontSize: '11px', color: 'var(--text-subtle)' }}>
            Ready to execute via <code>pytest</code> or <code>npx playwright test</code>
          </span>
        </div>
        <pre className="code-content">{currentCode}</pre>
      </div>
    </div>
  );
}
