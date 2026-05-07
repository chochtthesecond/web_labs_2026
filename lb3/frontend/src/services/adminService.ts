import { api } from './api';
import {
  StudentOut,
  StudentCreateWithUser,
  StudentUpdate,
  CourseOut,
  CourseCreate,
  CourseUpdate,
  EnrollmentStats,
} from '../types/admin';

export const adminService = {
  //студенты
  getStudents: async (page: number = 1, limit: number = 100): Promise<StudentOut[]> => {
    const response = await api.get(`/admin/students`, { params: { page, limit } });
    return response.data;
  },

  getStudent: async (id: number): Promise<StudentOut> => {
    const response = await api.get(`/admin/students/${id}`);
    return response.data;
  },

  createStudent: async (data: StudentCreateWithUser): Promise<StudentOut> => {
    const response = await api.post('/admin/students', data);
    return response.data;
  },

  updateStudent: async (id: number, data: StudentUpdate): Promise<StudentOut> => {
    const response = await api.put(`/admin/students/${id}`, data);
    return response.data;
  },

  deleteStudent: async (id: number): Promise<void> => {
    await api.delete(`/admin/students/${id}`);
  },

  //курсы
  getCourses: async (page: number = 1, limit: number = 100): Promise<CourseOut[]> => {
    const response = await api.get(`/admin/courses`, { params: { page, limit } });
    return response.data;
  },

  getCourse: async (id: number): Promise<CourseOut> => {
    const response = await api.get(`/admin/courses/${id}`);
    return response.data;
  },

  createCourse: async (data: CourseCreate): Promise<CourseOut> => {
    const response = await api.post('/admin/courses', data);
    return response.data;
  },

  updateCourse: async (id: number, data: CourseUpdate): Promise<CourseOut> => {
    const response = await api.put(`/admin/courses/${id}`, data);
    return response.data;
  },

  deleteCourse: async (id: number): Promise<void> => {
    await api.delete(`/admin/courses/${id}`);
  },

  //зачисления
  enrollStudent: async (studentId: number, courseId: number): Promise<void> => {
    await api.post('/admin/enrollments', { student_id: studentId, course_id: courseId });
  },

  unenrollStudent: async (studentId: number, courseId: number): Promise<void> => {
    await api.delete(`/admin/enrollments/${studentId}/${courseId}`);
  },
};