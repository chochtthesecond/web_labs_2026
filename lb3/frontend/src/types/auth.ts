export interface User {
  id: number;
  email: string;
  role: 'admin' | 'student';
  name: string;
  phone?: string;
  created_at: string;
}

export interface LoginCredentials {
  username: string;  //email
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  phone?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface Course {
  id: number;
  title: string;
  description: string | null;
  teacher: string | null;
  created_at: string;
}

export interface CourseWithEnrolled extends Course {
  isEnrolled: boolean;
}

export interface MyCourse extends Course {
  enrolled_at: string;
}