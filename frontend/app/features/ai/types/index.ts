export interface AISummary {
  id: string;
  sourceId: string;
  sourceType: 'note' | 'voice';
  title: string;
  summary: string;
  keyPoints: string[];
  confidence: number; // 0-1
  createdAt: Date;
}

export interface AIInsight {
  id: string;
  type: 'pattern' | 'suggestion' | 'reminder';
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  actionable: boolean;
  createdAt: Date;
}

export interface AISettings {
  autoSummarize: boolean;
  generateInsights: boolean;
  summaryLength: 'short' | 'medium' | 'long';
}