import React, { useState } from 'react';
import { Play, ChevronDown, ChevronUp, FileCode, CheckCircle2, AlertTriangle, ShieldCheck, Activity, Loader2 } from 'lucide-react';

export default function TestCaseViewer({ 
  testSuite, 
  onRunTest, 
  runningTestId, 
  executionResults = {} 
}) {
  const [activeCategory, setActiveCategory] = useState('all');
  const [expandedId, setExpandedId] = useState(null);
  const [showGherkinId, setShowGherkinId] = useState(null);

  if (!testSuite || !testSuite.test_cases) return null;

  const testCases = testSuite.test_cases;
  const categories = ['all', 'smoke', 'edge_case', 'regression', 'security'];

  const filteredTests = activeCategory === 'all' 
    ? testCases 
    : testCases.filter(tc => tc.category === activeCategory);

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const toggleGherkin = (id, e) => {
    e.stopPropagation();
    setShowGherkinId(showGherkinId === id ? null : id);
  };

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={20} color="var(--accent-cyan)" />
            <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Generated QA Test Suite</h2>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
            {testSuite.summary} (Generated via <i>{testSuite.model_used}</i>)
          </p>
        </div>

        {/* Category Filter Pills */}
        <div style={{ display: 'flex', gap: '6px' }}>
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              className={`preset-pill ${activeCategory === cat ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat)}
            >
              {cat === 'all' ? 'All Tests' : cat.replace('_', ' ').toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Test Case Cards */}
      <div className="test-cards-list">
        {filteredTests.map((tc) => {
          const isExpanded = expandedId === tc.id;
          const isRunning = runningTestId === tc.id;
          const result = executionResults[tc.id];

          return (
            <div key={tc.id} className="test-card">
              <div className="test-card-header" onClick={() => toggleExpand(tc.id)}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                    {tc.id}
                  </span>
                  <span className={`category-tag ${tc.category}`}>
                    {tc.category.replace('_', ' ')}
                  </span>
                  <span className="test-title">{tc.title}</span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  {/* Status badge from recent execution */}
                  {result && (
                    <span style={{ 
                      fontSize: '12px', 
                      fontWeight: 700, 
                      padding: '3px 10px', 
                      borderRadius: '9999px',
                      background: result.status === 'passed' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)',
                      color: result.status === 'passed' ? '#34d399' : '#fb7185',
                      border: `1px solid ${result.status === 'passed' ? 'rgba(16, 185, 129, 0.4)' : 'rgba(244, 63, 94, 0.4)'}`
                    }}>
                      {result.status === 'passed' ? 'PASSED' : 'BUG FOUND'}
                    </span>
                  )}

                  {/* Run Live Test Action */}
                  <button
                    type="button"
                    className="btn btn-primary btn-sm"
                    disabled={isRunning}
                    onClick={(e) => {
                      e.stopPropagation();
                      onRunTest(tc);
                    }}
                  >
                    {isRunning ? (
                      <>
                        <Loader2 size={13} style={{ animation: 'spin 1s linear infinite' }} />
                        Executing...
                      </>
                    ) : (
                      <>
                        <Play size={13} />
                        Run Live Test
                      </>
                    )}
                  </button>

                  <button
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={(e) => toggleGherkin(tc.id, e)}
                    title="Toggle Gherkin BDD Syntax"
                  >
                    <FileCode size={13} />
                    BDD
                  </button>

                  {isExpanded ? <ChevronUp size={16} color="var(--text-muted)" /> : <ChevronDown size={16} color="var(--text-muted)" />}
                </div>
              </div>

              {/* Gherkin drawer */}
              {showGherkinId === tc.id && tc.gherkin && (
                <div style={{ padding: '12px 20px', background: 'rgba(0,0,0,0.5)', borderTop: '1px solid var(--border-subtle)', fontFamily: 'var(--font-mono)', fontSize: '12px', color: '#38bdf8', whiteSpace: 'pre-wrap' }}>
                  {tc.gherkin}
                </div>
              )}

              {/* Expanded details */}
              {isExpanded && (
                <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border-subtle)', background: 'rgba(0,0,0,0.2)' }}>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '12px' }}>
                    {tc.description}
                  </p>

                  <div style={{ marginBottom: '12px' }}>
                    <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-subtle)' }}>Preconditions: </span>
                    <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{tc.preconditions.join(' • ')}</span>
                  </div>

                  <table className="test-steps-table">
                    <thead>
                      <tr>
                        <th style={{ width: '60px' }}>Step</th>
                        <th style={{ width: '100px' }}>Action</th>
                        <th>Target Element</th>
                        <th>Input Value</th>
                        <th>Expected Outcome</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tc.steps.map((st) => (
                        <tr key={st.step_number}>
                          <td style={{ fontWeight: 700, color: 'var(--text-subtle)' }}>#{st.step_number}</td>
                          <td>
                            <span style={{ fontSize: '11px', fontWeight: 700, padding: '2px 6px', borderRadius: '4px', background: 'rgba(255,255,255,0.06)', color: '#fff' }}>
                              {st.action.toUpperCase()}
                            </span>
                          </td>
                          <td><code>{st.target}</code></td>
                          <td>{st.value ? <code>"{st.value}"</code> : <span style={{ color: 'var(--text-subtle)' }}>—</span>}</td>
                          <td style={{ color: 'var(--text-muted)' }}>{st.expected_outcome}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  <div style={{ marginTop: '12px', padding: '10px 14px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '6px', border: '1px solid rgba(16, 185, 129, 0.2)', fontSize: '13px', color: '#34d399' }}>
                    <b>Expected Verification:</b> {tc.expected_result}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
