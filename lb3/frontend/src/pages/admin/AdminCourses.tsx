import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { adminService } from '../../services/adminService';
import { CourseOut } from '../../types/admin';
import styles from '../../styles/courses.module.css';

const AdminCourses: React.FC = () => {
  const [courses, setCourses] = useState<CourseOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCourses = async () => {
    try {
      setLoading(true);
      const data = await adminService.getCourses();
      setCourses(data);
    } catch (err: any) {
      setError(err.message || 'Ошибка загрузки курсов');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourses();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить курс? Все связанные зачисления будут удалены.')) return;
    try {
      await adminService.deleteCourse(id);
      await loadCourses();
    } catch (err: any) {
      alert('Ошибка удаления: ' + err.message);
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles['courses-list']}>
      <h1>Управление курсами</h1>
      <Link to="/admin/courses/new" className={styles.btn}>
        Добавить курс
      </Link>

      <div className={styles['table-wrapper']}>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Описание</th>
              <th>Преподаватель</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((course) => (
              <tr key={course.id}>
                <td>{course.id}</td>
                <td>{course.title}</td>
                <td>{course.description || '—'}</td>
                <td>{course.teacher || '—'}</td>
                <td>
                  <Link to={`/admin/courses/${course.id}/edit`}>Редактировать</Link>
                  <button onClick={() => handleDelete(course.id)}>Удалить</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminCourses;