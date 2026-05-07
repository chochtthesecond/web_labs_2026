import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { RoleRoute } from './components/RoleRoute';
import Layout from './components/Layout';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import Profile from './pages/Profile';
import Courses from './pages/Courses';
import MyCourses from './pages/MyCourses';
import AdminStudents from './pages/admin/AdminStudents';
import AdminStudentForm from './pages/admin/AdminStudentForm';
import AdminCourses from './pages/admin/AdminCourses';
import AdminCourseForm from './pages/admin/AdminCourseForm';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
		<Layout>
        <Routes>
			{/*Public*/}
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/*Protected*/}
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
            <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} />
            <Route path="/my-courses" element={<ProtectedRoute><MyCourses /></ProtectedRoute>} />

            {/*Admin*/}
            <Route path="/admin/students" element={<RoleRoute allowedRoles={['admin']}><AdminStudents /></RoleRoute>} />
            <Route path="/admin/students/new" element={<RoleRoute allowedRoles={['admin']}><AdminStudentForm /></RoleRoute>} />
            <Route path="/admin/students/:id/edit" element={<RoleRoute allowedRoles={['admin']}><AdminStudentForm /></RoleRoute>} />
            <Route path="/admin/courses" element={<RoleRoute allowedRoles={['admin']}><AdminCourses /></RoleRoute>} />
            <Route path="/admin/courses/new" element={<RoleRoute allowedRoles={['admin']}><AdminCourseForm /></RoleRoute>} />
            <Route path="/admin/courses/:id/edit" element={<RoleRoute allowedRoles={['admin']}><AdminCourseForm /></RoleRoute>} />

            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
		</Layout>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;