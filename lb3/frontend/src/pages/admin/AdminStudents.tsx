import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { adminService } from '../../services/adminService';
import { StudentOut } from '../../types/admin';
import styles from '../../styles/students.module.css';

const AdminStudents: React.FC = () => {
  const [students, setStudents] = useState<StudentOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadStudents = async () => {
    try {
      setLoading(true);
      const data = await adminService.getStudents();
      setStudents(data);
    } catch (err: any) {
      setError(err.message || 'Ошибка загрузки студентов');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStudents();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить студента? Это действие также удалит связанного пользователя и все зачисления.')) return;
    try {
      await adminService.deleteStudent(id);
      await loadStudents();
    } catch (err: any) {
      alert('Ошибка удаления: ' + err.message);
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <section className={styles['students-list']}>
      <h1>Управление студентами</h1>
      <Link to="/admin/students/new" className={styles.btn}>
        Добавить студента
      </Link>
      <div className={styles['table-wrapper']}>
        <table className={styles['data-table']}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя</th>
              <th>Email</th>
              <th>Телефон</th>
              <th>Дата регистрации</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {students.map((student) => (
              <tr key={student.id}>
                <td>{student.id}</td>
                <td>{student.name}</td>
                <td>{student.email}</td>
                <td>{student.phone || '—'}</td>
                <td>{new Date(student.created_at).toLocaleDateString()}</td>
                <td>
                  <Link to={`/admin/students/${student.id}/edit`}>
                    Редактировать
                  </Link>
                  <button onClick={() => handleDelete(student.id)}>
                    Удалить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default AdminStudents;