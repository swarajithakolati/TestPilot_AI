/**
 * TestPilot AI Frontend API Service Client
 * Provides centralized, type-safe communication with the FastAPI backend.
 */

const API_BASE = ''; // Proxied by Vite to http://127.0.0.1:8000

export async function checkApiHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return await res.json();
}

export async function fetchPresets() {
  const res = await fetch(`${API_BASE}/api/presets`);
  if (!res.ok) throw new Error(`Presets request failed: ${res.statusText}`);
  return await res.json();
}

export async function inspectPageDom(url, waitTimeMs = 2000) {
  const res = await fetch(`${API_BASE}/api/inspect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, wait_time_ms: waitTimeMs })
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function generateTestSuite(payload) {
  const res = await fetch(`${API_BASE}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function executeLiveTest(payload) {
  const res = await fetch(`${API_BASE}/api/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}
