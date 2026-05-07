import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { adminService } from '../../services/adminService';
import { StudentOut, StudentCreateWithUser, StudentUpdate } from '../../types/admin';
import styles from '../../styles/student_form.module.css';

const AdminStudentForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = !!id;

  const [formData, setFormData] = useState<StudentCreateWithUser | StudentUpdate>({
    name: '',
    email: '',
    password: '',
    phone: '',
    role: 'student',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isEditing) {
      const loadStudent = async () => {
        try {
          const student = await adminService.getStudent(Number(id));
          setFormData({
            name: student.name,
            email: student.email,
            phone: student.phone || '',
          } as StudentUpdate);
        } catch (err: any) {
          setError(err.message);
        }
      };
      loadStudent();
    }
  }, [id, isEditing]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEditing) {
        const { name, phone } = formData as StudentUpdate;
        await adminService.updateStudent(Number(id), { name, phone });
      } else {
        await adminService.createStudent(formData as StudentCreateWithUser);
      }
      navigate('/admin/students');
    } catch (err: any) {
      alert('Ошибка сохранения: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles['student-form']}>
      <h1>{isEditing ? 'Редактирование студента' : 'Добавление студента'}</h1>
      {error && <div className={styles.error}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Имя *</label>
          <input
            type="text"
            name="name"
            value={formData.name || ''}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Email *</label>
          <input
            type="email"
            name="email"
            value={formData.email || ''}
            onChange={handleChange}
            required
            disabled={isEditing}
          />
        </div>
        {!isEditing && (
          <div>
            <label>Пароль *</label>
            <input
              type="password"
              name="password"
              value={(formData as StudentCreateWithUser).password || ''}
              onChange={handleChange}
              required
            />
          </div>
        )}
        <div>
          <label>Телефон</label>
          <input
            type="text"
            name="phone"
            value={formData.phone || ''}
            onChange={handleChange}
          />
        </div>
        {!isEditing && (
          <div>
            <label>Роль</label>
            <select name="role" value={(formData as StudentCreateWithUser).role || 'student'} onChange={handleChange}>
              <option value="student">Студент</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
        )}
		<div className={styles.buttons}>
        <button type="submit" disabled={loading}>
          {loading ? 'Сохранение...' : 'Сохранить'}
        </button>
        <Link to="/admin/students">Отмена</Link>
		</div>
      </form>
    </div>
  );
};

export default AdminStudentForm;