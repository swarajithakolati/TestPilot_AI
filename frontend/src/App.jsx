import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import UrlBar from './components/UrlBar';
import DomInspector from './components/DomInspector';
import TestCaseViewer from './components/TestCaseViewer';
import CodeViewer from './components/CodeViewer';
import LiveRunner from './components/LiveRunner';
import BugReportModal from './components/BugReportModal';
import { Layers, Activity, Code2, Terminal } from 'lucide-react';

export default function App() {
  const [url, setUrl] = useState('http://127.0.0.1:8000/demo/shop');
  const [presets, setPresets] = useState([]);
  const [headed, setHeaded] = useState(false);
  const [provider, setProvider] = useState('hybrid');
  const [apiKey, setApiKey] = useState('');
  const [apiHealth, setApiHealth] = useState(null);

  const [loading, setLoading] = useState(false);
  const [inspection, setInspection] = useState(null);
  const [testSuite, setTestSuite] = useState(null);

  const [activeTab, setActiveTab] = useState('testcases');
  const [runningTestId, setRunningTestId] = useState(null);
  const [activeTestCase, setActiveTestCase] = useState(null);
  const [currentExecution, setCurrentExecution] = useState(null);
  const [executionResults, setExecutionResults] = useState({});
  const [activeBugReport, setActiveBugReport] = useState(null);

  // Fetch presets and health on mount
  useEffect(() => {
    fetch('/api/presets')
      .then(res => res.json())
      .then(data => {
        setPresets(data);
        if (data.length > 0 && !url) {
          setUrl(data[0].url);
        }
      })
      .catch(err => console.error('Failed to load presets:', err));

    fetch('/api/health')
      .then(res => res.json())
      .then(data => setApiHealth(data))
      .catch(err => console.error('Failed to check health:', err));
  }, []);

  // Inspect page DOM only
  const handleInspectOnly = async (targetUrl) => {
    setLoading(true);
    try {
      const res = await fetch('/api/inspect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: targetUrl, wait_time_ms: 2000 })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setInspection(data);
      setActiveTab('dom');
    } catch (err) {
      alert(`Inspection Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Inspect and generate test suite
  const handleInspectAndGenerate = async (targetUrl, instructions) => {
    setLoading(true);
    try {
      // Step 1: Inspect DOM
      const inspRes = await fetch('/api/inspect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: targetUrl, wait_time_ms: 2000 })
      });
      if (!inspRes.ok) throw new Error(await inspRes.text());
      const inspData = await inspRes.json();
      setInspection(inspData);

      // Step 2: Generate Test Suite
      const genRes = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: targetUrl,
          inspection: inspData,
          custom_instructions: instructions,
          gemini_api_key: apiKey.startsWith('AIza') ? apiKey : undefined,
          openai_api_key: apiKey.startsWith('sk-') ? apiKey : undefined,
          provider: provider
        })
      });
      if (!genRes.ok) throw new Error(await genRes.text());
      const suiteData = await genRes.json();
      setTestSuite(suiteData);
      setActiveTab('testcases');
    } catch (err) {
      alert(`Generation Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Execute test live
  const handleRunTest = async (testCase) => {
    setRunningTestId(testCase.id);
    setActiveTestCase(testCase);
    setCurrentExecution({ status: 'running', steps: [] });
    setActiveTab('runner');

    try {
      const res = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: url,
          test_case_id: testCase.id,
          test_case: testCase,
          headed: headed
        })
      });
      if (!res.ok) throw new Error(await res.text());
      const result = await res.json();
      
      setCurrentExecution(result);
      setExecutionResults(prev => ({ ...prev, [testCase.id]: result }));

      // If test failed with bug report, auto-open bug modal after slight delay
      if (result.bug_report) {
        setTimeout(() => {
          setActiveBugReport(result.bug_report);
        }, 800);
      }
    } catch (err) {
      setCurrentExecution({
        status: 'failed',
        steps: [{ step_index: 1, description: 'Runner Execution', status: 'failed', error_message: err.message }]
      });
    } finally {
      setRunningTestId(null);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <Header
        headed={headed}
        setHeaded={setHeaded}
        provider={provider}
        setProvider={setProvider}
        apiKey={apiKey}
        setApiKey={setApiKey}
        apiHealth={apiHealth}
      />

      {/* Hero URL Input & Presets Bar */}
      <UrlBar
        url={url}
        setUrl={setUrl}
        onInspectAndGenerate={handleInspectAndGenerate}
        onInspectOnly={handleInspectOnly}
        loading={loading}
        presets={presets}
      />

      {/* Workspace Tabs */}
      {(inspection || testSuite || currentExecution) && (
        <div>
          <div className="tabs-bar" style={{ marginBottom: '20px' }}>
            {testSuite && (
              <button
                type="button"
                className={`tab-btn ${activeTab === 'testcases' ? 'active' : ''}`}
                onClick={() => setActiveTab('testcases')}
              >
                <Activity size={16} />
                Test Cases ({testSuite.test_cases?.length || 0})
              </button>
            )}

            {inspection && (
              <button
                type="button"
                className={`tab-btn ${activeTab === 'dom' ? 'active' : ''}`}
                onClick={() => setActiveTab('dom')}
              >
                <Layers size={16} />
                DOM Elements ({inspection.elements_count || 0})
              </button>
            )}

            {testSuite && (
              <button
                type="button"
                className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
                onClick={() => setActiveTab('code')}
              >
                <Code2 size={16} />
                Automation Scripts (Python & TS)
              </button>
            )}

            {(currentExecution || runningTestId) && (
              <button
                type="button"
                className={`tab-btn ${activeTab === 'runner' ? 'active' : ''}`}
                onClick={() => setActiveTab('runner')}
              >
                <Terminal size={16} />
                Live Runner Telemetry
              </button>
            )}
          </div>

          {/* Active Tab Content */}
          {activeTab === 'testcases' && testSuite && (
            <TestCaseViewer
              testSuite={testSuite}
              onRunTest={handleRunTest}
              runningTestId={runningTestId}
              executionResults={executionResults}
            />
          )}

          {activeTab === 'dom' && inspection && (
            <DomInspector inspection={inspection} />
          )}

          {activeTab === 'code' && testSuite && (
            <CodeViewer testSuite={testSuite} />
          )}

          {activeTab === 'runner' && (
            <LiveRunner
              currentExecution={currentExecution}
              activeTestCase={activeTestCase}
              onOpenBugReport={() => setActiveBugReport(currentExecution?.bug_report)}
            />
          )}
        </div>
      )}

      {/* Bug Report Modal */}
      {activeBugReport && (
        <BugReportModal
          bugReport={activeBugReport}
          onClose={() => setActiveBugReport(null)}
        />
      )}
    </div>
  );
}
