import { api } from './api';
import { User } from '../types/auth';

export const studentService = {
  getProfile: async (): Promise<User> => {
    const response = await api.get('/students/me');
    return response.data;
  },

  updateProfile: async (data: { name: string; phone?: string }): Promise<User> => {
    const response = await api.put('/students/me', data);
    return response.data;
  },
};