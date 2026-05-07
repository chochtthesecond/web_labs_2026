import { api } from './api';
import { Course, MyCourse } from '../types/auth';

export const courseService = {
  //список всех курсов
  getAll: async (): Promise<Course[]> => {
    const response = await api.get('/courses');
    return response.data;
  },

  //курсы на которые записан студент
  getMyCourses: async (): Promise<MyCourse[]> => {
    const response = await api.get('/courses/me');
    return response.data;
  },

  //записаться на курс
  enroll: async (courseId: number): Promise<void> => {
    await api.post(`/courses/${courseId}/enroll`);
  },

  //отписаться от курса
  withdraw: async (courseId: number): Promise<void> => {
    await api.delete(`/courses/${courseId}/enroll`);
  },
};