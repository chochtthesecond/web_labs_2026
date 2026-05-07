import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface Props {
  children: JSX.Element;
  allowedRoles: Array<'admin' | 'student'>;
}

export const RoleRoute = ({ children, allowedRoles }: Props) => {
  const { user, loading } = useAuth();
  if (loading) return <div>Загрузка...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (!allowedRoles.includes(user.role)) {
    //если роль не подходит перенаправляем на главную
    return <Navigate to="/" replace />;
  }
  return children;
};