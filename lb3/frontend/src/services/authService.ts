import { api } from './api';
import { User, LoginCredentials, RegisterData, AuthTokens } from '../types/auth';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    const { data } = await api.post<AuthTokens>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return data;
  },

  async register(data: RegisterData): Promise<User> {
    const { data: user } = await api.post<User>('/auth/register', data);
    return user;
  },

  async getMe(): Promise<User> {
    const { data } = await api.get<User>('/auth/me');
    return data;
  },

  async refresh(refreshToken: string): Promise<{ access_token: string }> {
    const { data } = await api.post<{ access_token: string }>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return data;
  },
};