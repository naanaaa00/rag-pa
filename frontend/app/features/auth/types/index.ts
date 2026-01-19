export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role?: 'user' | 'admin';
}

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthError {
  message: string;
  code?: string;
}