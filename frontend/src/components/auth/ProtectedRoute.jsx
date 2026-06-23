import { Navigate } from "react-router-dom"
import { useSelector } from "react-redux"

export default function ProtectedRoute({ children, allowedRoles }) {
  const { isAuthenticated, role } = useSelector((state) => state.auth)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    if (role === "CUSTOMER") {
      return <Navigate to="/orders" replace />
    }
    return <Navigate to="/" replace />
  }

  return children
}
