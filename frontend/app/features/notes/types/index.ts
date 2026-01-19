export interface Note {
  id: string;
  title: string;
  content: string;
  excerpt?: string;
  type: 'text' | 'voice' | 'meeting' | 'documentation';
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  isArchived: boolean;
  isFavorite: boolean;
}

export interface CreateNoteData {
  title: string;
  content: string;
  type: Note['type'];
  tags?: string[];
}

export interface UpdateNoteData {
  title?: string;
  content?: string;
  tags?: string[];
}

export type NotesFilter = 'all' | 'text' | 'voice' | 'meeting' | 'documentation';
export type NotesSortBy = 'createdAt' | 'updatedAt' | 'title';
export type NotesSortOrder = 'asc' | 'desc';