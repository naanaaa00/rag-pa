import { useAuthStore } from '../stores/auth-store';

// Selector hooks untuk specific data
export const useUser = () => useAuthStore(state => state.user);
export const useIsAuthenticated = () => useAuthStore(state => state.isAuthenticated);
export const useAuthLoading = () => useAuthStore(state => state.isLoading);

// Action hooks
export const useAuthActions = () => {
  const login = useAuthStore(state => state.login);
  const logout = useAuthStore(state => state.logout);
  const setUser = useAuthStore(state => state.setUser);
  
  return { login, logout, setUser };
};