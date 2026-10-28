import React from 'react';
import { Terminal, CheckCircle2, XCircle, AlertTriangle, Bug, Clock, Loader2, Sparkles } from 'lucide-react';

export default function LiveRunner({ 
  currentExecution, 
  activeTestCase, 
  onOpenBugReport 
}) {
  if (!currentExecution && !activeTestCase) return null;

  const isRunning = currentExecution?.status === 'running';
  const isFailed = currentExecution?.status === 'failed';
  const isPassed = currentExecution?.status === 'passed';

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Terminal size={20} color="var(--accent-cyan)" />
          <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Live Browser Execution Telemetry</h2>
        </div>

        {currentExecution && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-subtle)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Clock size={12} />
              {currentExecution.duration_seconds ? `${currentExecution.duration_seconds}s` : 'In Progress'}
            </span>
            <span style={{ 
              fontSize: '11px', 
              fontWeight: 800, 
              padding: '3px 10px', 
              borderRadius: '9999px',
              textTransform: 'uppercase',
              background: isPassed ? 'rgba(16, 185, 129, 0.2)' : isFailed ? 'rgba(244, 63, 94, 0.2)' : 'rgba(56, 189, 248, 0.2)',
              color: isPassed ? '#34d399' : isFailed ? '#fb7185' : '#38bdf8',
              border: `1px solid ${isPassed ? 'rgba(16, 185, 129, 0.4)' : isFailed ? 'rgba(244, 63, 94, 0.4)' : 'rgba(56, 189, 248, 0.4)'}`
            }}>
              {isRunning && 'RUNNING PLAYWRIGHT...'}
              {isPassed && 'ALL CHECKS PASSED'}
              {isFailed && 'DEFECT DETECTED'}
            </span>
          </div>
        )}
      </div>

      {/* Terminal Display */}
      <div className="terminal-window">
        <div className="terminal-header">
          <div className="traffic-dots">
            <span className="dot red"></span>
            <span className="dot yellow"></span>
            <span className="dot green"></span>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-subtle)', fontFamily: 'var(--font-mono)' }}>
            Playwright Test Runner — {activeTestCase ? activeTestCase.title : 'Idle'}
          </span>
          <span style={{ fontSize: '11px', color: 'var(--accent-cyan)' }}>
            chromium-headless-shell
          </span>
        </div>

        <div className="terminal-body">
          {(!currentExecution?.steps || currentExecution.steps.length === 0) && (
            <div className="terminal-line running">
              <span className="time">[0.00s]</span>
              <span>Initializing browser context and loading page...</span>
            </div>
          )}

          {currentExecution?.steps?.map((step) => (
            <div key={step.step_index} className={`terminal-line ${step.status}`}>
              <span className="time">[{step.duration_ms ? `${step.duration_ms}ms` : '...'}]</span>
              <span>
                {step.status === 'passed' && '✓ '}
                {step.status === 'failed' && '✗ '}
                {step.status === 'running' && '➜ '}
                {step.description}
              </span>
              {step.error_message && (
                <div style={{ color: '#fb7185', fontSize: '12px', marginTop: '2px', paddingLeft: '16px' }}>
                  → Error: {step.error_message}
                </div>
              )}
            </div>
          ))}

          {currentExecution?.console_logs?.map((c, i) => (
            <div key={`c-${i}`} className="terminal-line info" style={{ fontSize: '11px', color: 'var(--text-subtle)' }}>
              <span className="time">[Console]</span>
              <span>{c}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Bug Alert Banner if Defect Found */}
      {isFailed && currentExecution?.bug_report && (
        <div style={{ 
          marginTop: '16px', 
          padding: '16px 20px', 
          background: 'rgba(244, 63, 94, 0.12)', 
          border: '1px solid rgba(244, 63, 94, 0.35)', 
          borderRadius: '10px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'rgba(244, 63, 94, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fb7185' }}>
              <Bug size={22} />
            </div>
            <div>
              <div style={{ fontSize: '14px', fontWeight: 700, color: '#fff' }}>
                {currentExecution.bug_report.title}
              </div>
              <p style={{ fontSize: '12px', color: '#fca5a5', marginTop: '2px' }}>
                {currentExecution.bug_report.root_cause_hypothesis}
              </p>
            </div>
          </div>

          <button 
            type="button"
            className="btn btn-danger"
            onClick={onOpenBugReport}
          >
            <Bug size={14} />
            View Defect Report & Reproduction Script
          </button>
        </div>
      )}

      {/* Passed Banner */}
      {isPassed && (
        <div style={{ 
          marginTop: '16px', 
          padding: '14px 20px', 
          background: 'rgba(16, 185, 129, 0.1)', 
          border: '1px solid rgba(16, 185, 129, 0.3)', 
          borderRadius: '10px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}>
          <CheckCircle2 size={20} color="var(--accent-emerald)" />
          <span style={{ fontSize: '14px', fontWeight: 600, color: '#34d399' }}>
            Test passed successfully! All UI assertions satisfied without runtime defects.
          </span>
        </div>
      )}
    </div>
  );
}
