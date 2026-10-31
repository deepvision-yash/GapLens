import { mockApi, isDemoMode } from '@/services/mockApi';

// API base URL
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types (re-export from types)
export type {
  ResearchSession,
  ResearchResultsResponse,
  SourceResponse,
  ClaimResponse,
  GapResponse,
  ConflictResponse,
  VerificationTaskResponse,
  SessionStatus,
  Priority,
  ResearchDimension,
  CoverageStatus,
  FindingStatus,
} from '@/types/research';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Research session endpoints
  async createResearch(payload: { goal: string; sources?: any[] }) {
    if (isDemoMode()) {
      return mockApi.createResearch(payload);
    }
    return this.request<{ id: string; status: string }>('/api/research', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async understandGoal(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.understandGoal(sessionId);
    }
    return this.request<{
      sessionId: string;
      goalUnderstanding: any;
      dimensions: any[];
      status: string;
    }>(`/api/research/${sessionId}/understand`, { method: 'POST' });
  }

  async getScope(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getScope(sessionId);
    }
    return this.request(`/api/research/${sessionId}/scope`);
  }

  async updateScope(sessionId: string, dimensions: any[]) {
    if (isDemoMode()) {
      return mockApi.updateScope(sessionId, dimensions);
    }
    return this.request(`/api/research/${sessionId}/scope`, {
      method: 'PATCH',
      body: JSON.stringify({ dimensions }),
    });
  }

  async startResearch(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.startResearch(sessionId);
    }
    return this.request(`/api/research/${sessionId}/start`, { method: 'POST' });
  }

  async getStatus(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getStatus(sessionId);
    }
    return this.request(`/api/research/${sessionId}/status`);
  }

  async getResults(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getResults(sessionId);
    }
    return this.request(`/api/research/${sessionId}/results`);
  }

  async getSources(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getSources(sessionId);
    }
    return this.request(`/api/research/${sessionId}/sources`);
  }

  async getClaims(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getClaims(sessionId);
    }
    return this.request(`/api/research/${sessionId}/claims`);
  }

  async getGaps(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getGaps(sessionId);
    }
    return this.request(`/api/research/${sessionId}/gaps`);
  }

  async getConflicts(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getConflicts(sessionId);
    }
    return this.request(`/api/research/${sessionId}/conflicts`);
  }

  async getChecklist(sessionId: string) {
    if (isDemoMode()) {
      return mockApi.getChecklist(sessionId);
    }
    return this.request(`/api/research/${sessionId}/checklist`);
  }

  async updateChecklistTask(sessionId: string, taskId: string, completed: boolean) {
    if (isDemoMode()) {
      return mockApi.updateChecklistTask(sessionId, taskId, completed);
    }
    return this.request(`/api/research/${sessionId}/checklist/${taskId}`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }

  // SSE event stream
  async *streamEvents(sessionId: string): AsyncGenerator<{ event: string; data: string }> {
    if (isDemoMode()) {
      for await (const event of mockApi.streamEvents(sessionId)) {
        yield event;
      }
      return;
    }

    const response = await fetch(`${this.baseUrl}/api/research/${sessionId}/events`, {
      headers: { Accept: 'text/event-stream' },
    });

    if (!response.ok) {
      throw new Error('Failed to connect to event stream');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No response body');
    }

    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('event:')) {
          const event = line.slice(6).trim();
          const dataLine = lines.shift();
          if (dataLine?.startsWith('data:')) {
            const data = dataLine.slice(5).trim();
            yield { event, data };
          }
        }
      }
    }
  }
}

export const api = new ApiClient();

// Helper to switch demo mode
export function setDemoMode(enabled: boolean) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('demoMode', enabled.toString());
  }
}

export function getDemoMode(): boolean {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('demoMode') === 'true';
  }
  return process.env.NEXT_PUBLIC_DEMO_MODE === 'true';
}