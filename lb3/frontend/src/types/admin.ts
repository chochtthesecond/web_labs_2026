export interface StudentOut {
  id: number;
  name: string;
  phone: string;
  created_at: string; //ISO
  email: string;
  role: 'admin' | 'student';
  user_id: number;
}

export interface StudentCreateWithUser {
  email: string;
  password: string;
  name: string;
  phone?: string;
  role?: 'student';
}

export interface StudentUpdate {
  name?: string;
  phone?: string;
}

export interface CourseOut {
  id: number;
  title: string;
  description?: string;
  teacher?: string;
  created_at: string;
}

export interface CourseCreate {
  title: string;
  description?: string;
  teacher?: string;
}

export interface CourseUpdate {
  title?: string;
  description?: string;
  teacher?: string;
}