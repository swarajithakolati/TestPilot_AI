import React, { useState } from 'react';
import { AlertCircle, Download, Copy, Check, FileCode, Wrench, Bug, ExternalLink } from 'lucide-react';

export default function BugReportModal({ bugReport, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!bugReport) return null;

  const handleCopyScript = () => {
    navigator.clipboard.writeText(bugReport.reproduce_script || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadScript = () => {
    const blob = new Blob([bugReport.reproduce_script || ''], { type: 'text/x-python;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `reproduce_${bugReport.bug_id.toLowerCase()}.py`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const severityColor = {
    critical: '#f43f5e',
    high: '#fb923c',
    medium: '#facc15',
    low: '#38bdf8'
  }[bugReport.severity.toLowerCase()] || '#f43f5e';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '860px' }}>
        {/* Modal Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '18px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <span style={{ 
                background: `rgba(${bugReport.severity === 'critical' ? '244, 63, 94' : '245, 158, 11'}, 0.15)`,
                color: severityColor,
                border: `1px solid ${severityColor}`,
                fontSize: '11px',
                fontWeight: 800,
                padding: '3px 10px',
                borderRadius: '9999px',
                textTransform: 'uppercase'
              }}>
                {bugReport.severity} Defect
              </span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', color: 'var(--text-subtle)' }}>
                {bugReport.bug_id}
              </span>
            </div>
            <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#fff' }}>{bugReport.title}</h2>
          </div>

          <button 
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '24px', cursor: 'pointer', lineHeight: 1 }}
          >
            &times;
          </button>
        </div>

        {/* Failed Step Context */}
        <div style={{ padding: '14px 18px', background: 'rgba(244, 63, 94, 0.08)', borderRadius: '10px', border: '1px solid rgba(244, 63, 94, 0.25)', marginBottom: '18px' }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: '#fb7185', textTransform: 'uppercase', marginBottom: '4px' }}>
            Failed Step Execution
          </div>
          <div style={{ fontSize: '14px', fontFamily: 'var(--font-mono)', color: '#fff', marginBottom: '8px' }}>
            {bugReport.failed_step}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '13px' }}>
            <div>
              <span style={{ color: 'var(--text-subtle)', display: 'block', fontSize: '11px', fontWeight: 600 }}>EXPECTED BEHAVIOR</span>
              <span style={{ color: '#34d399' }}>{bugReport.expected_behavior}</span>
            </div>
            <div>
              <span style={{ color: 'var(--text-subtle)', display: 'block', fontSize: '11px', fontWeight: 600 }}>ACTUAL BEHAVIOR</span>
              <span style={{ color: '#fb7185' }}>{bugReport.actual_behavior}</span>
            </div>
          </div>
        </div>

        {/* Defect Screenshot Preview */}
        {bugReport.screenshot_url && (
          <div style={{ marginBottom: '18px' }}>
            <span style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-subtle)', marginBottom: '6px' }}>
              DEFECT STATE SNAPSHOT
            </span>
            <div style={{ borderRadius: '10px', overflow: 'hidden', border: '1px solid var(--border-subtle)', maxHeight: '240px' }}>
              <img 
                src={bugReport.screenshot_url} 
                alt="Defect Failure Snapshot" 
                style={{ width: '100%', height: 'auto', display: 'block', objectFit: 'cover' }} 
              />
            </div>
          </div>
        )}

        {/* Diagnosis & Suggested Fix */}
        <div className="grid-2col" style={{ marginBottom: '20px' }}>
          <div style={{ padding: '14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: 'var(--accent-amber)', marginBottom: '6px' }}>
              <Bug size={14} />
              ROOT CAUSE HYPOTHESIS
            </div>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: 1.5 }}>
              {bugReport.root_cause_hypothesis}
            </p>
          </div>

          <div style={{ padding: '14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: 'var(--accent-emerald)', marginBottom: '6px' }}>
              <Wrench size={14} />
              ENGINEERING REMEDIATION
            </div>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: 1.5 }}>
              {bugReport.suggested_fix}
            </p>
          </div>
        </div>

        {/* Standalone Reproduction Script */}
        <div style={{ marginBottom: '18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-subtle)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <FileCode size={14} />
              AUTONOMOUS REPRODUCTION SCRIPT (PLAYWRIGHT PYTHON)
            </span>

            <div style={{ display: 'flex', gap: '6px' }}>
              <button type="button" className="btn btn-secondary btn-sm" onClick={handleCopyScript}>
                {copied ? <Check size={12} color="var(--accent-emerald)" /> : <Copy size={12} />}
                {copied ? 'Copied' : 'Copy'}
              </button>
              <button type="button" className="btn btn-primary btn-sm" onClick={handleDownloadScript}>
                <Download size={12} />
                Download Script
              </button>
            </div>
          </div>

          <pre style={{ 
            background: '#06090e', 
            borderRadius: '8px', 
            border: '1px solid var(--border-subtle)', 
            padding: '14px', 
            fontFamily: 'var(--font-mono)', 
            fontSize: '12px', 
            maxHeight: '220px', 
            overflowY: 'auto',
            color: '#e2e8f0',
            whiteSpace: 'pre'
          }}>
            {bugReport.reproduce_script}
          </pre>
        </div>

        {/* Console / Network Logs */}
        {bugReport.console_errors && bugReport.console_errors.length > 0 && (
          <div style={{ marginBottom: '18px', padding: '10px 14px', background: 'rgba(0,0,0,0.5)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-subtle)', display: 'block', marginBottom: '4px' }}>
              CAPTURED BROWSER CONSOLE ERRORS
            </span>
            {bugReport.console_errors.map((err, i) => (
              <div key={i} style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: '#fb7185' }}>
                {err}
              </div>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button className="btn btn-secondary" onClick={onClose}>Close Report</button>
        </div>
      </div>
    </div>
  );
}
