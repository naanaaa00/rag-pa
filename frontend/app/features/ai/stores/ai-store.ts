import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { AISummary, AIInsight, AISettings } from '../types';

interface AIState {
  summaries: AISummary[];
  insights: AIInsight[];
  isProcessing: boolean;
  settings: AISettings;
}

interface AIActions {
  generateSummary: (sourceId: string, sourceType: 'note' | 'voice', content: string) => Promise<void>;
  deleteSummary: (id: string) => void;
  dismissInsight: (id: string) => void;
  updateSettings: (settings: Partial<AISettings>) => void;
  setProcessing: (processing: boolean) => void;
}

// Mock data
const mockSummaries: AISummary[] = [
  {
    id: '1',
    sourceId: '1',
    sourceType: 'note',
    title: 'Project Planning Summary',
    summary: 'Team discussed Q1 roadmap and resource allocation.',
    keyPoints: ['Q1 roadmap finalized', 'Resource allocation completed'],
    confidence: 0.85,
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000)
  }
];

export const useAIStore = create<AIState & AIActions>()(
  devtools(
    (set) => ({
      // State
      summaries: mockSummaries,
      insights: [],
      isProcessing: false,
      settings: {
        autoSummarize: true,
        generateInsights: true,
        summaryLength: 'medium'
      },

      // Actions
      generateSummary: async (sourceId, sourceType, content) => {
        set({ isProcessing: true });
        
        try {
          // Simulate AI processing
          await new Promise(resolve => setTimeout(resolve, 2000));
          
          const summary: AISummary = {
            id: Date.now().toString(),
            sourceId,
            sourceType,
            title: `${sourceType === 'note' ? 'Note' : 'Recording'} Summary`,
            summary: 'AI-generated summary of the content.',
            keyPoints: ['Key point 1', 'Key point 2'],
            confidence: 0.8,
            createdAt: new Date()
          };

          set(state => ({
            summaries: [summary, ...state.summaries],
            isProcessing: false
          }));

        } catch (error) {
          set({ isProcessing: false });
        }
      },

      deleteSummary: (id: string) => {
        set(state => ({
          summaries: state.summaries.filter(s => s.id !== id)
        }));
      },

      dismissInsight: (id: string) => {
        set(state => ({
          insights: state.insights.filter(i => i.id !== id)
        }));
      },

      updateSettings: (newSettings) => {
        set(state => ({
          settings: { ...state.settings, ...newSettings }
        }));
      },

      setProcessing: (processing: boolean) => set({ isProcessing: processing })
    })
  )
);