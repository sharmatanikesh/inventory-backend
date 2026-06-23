import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { Toaster } from "react-hot-toast"
import AppLayout from "./components/layout/AppLayout"
import DashboardPage from "./components/dashboard/DashboardPage"
import ProductsPage from "./components/products/ProductsPage"
import CustomersPage from "./components/customers/CustomersPage"
import OrdersPage from "./components/orders/OrdersPage"
import CreateOrderPage from "./components/orders/CreateOrderPage"
import LoginPage from "./components/auth/LoginPage"
import ProtectedRoute from "./components/auth/ProtectedRoute"

export default function App() {
  return (
    <Router>
      <Toaster 
        position="top-right" 
        toastOptions={{
          style: {
            fontFamily: "Inter, sans-serif",
            fontSize: "13px",
            fontWeight: "500",
            borderRadius: "8px",
            background: "#fff",
            color: "#1e293b",
            boxShadow: "0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.05)",
            border: "1px solid #f1f5f9"
          }
        }}
      />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        <Route path="/" element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }>
          <Route index element={
            <ProtectedRoute allowedRoles={["ADMIN"]}>
              <DashboardPage />
            </ProtectedRoute>
          } />
          <Route path="products" element={
            <ProtectedRoute allowedRoles={["ADMIN"]}>
              <ProductsPage />
            </ProtectedRoute>
          } />
          <Route path="customers" element={
            <ProtectedRoute allowedRoles={["ADMIN"]}>
              <CustomersPage />
            </ProtectedRoute>
          } />
          <Route path="orders" element={
            <ProtectedRoute allowedRoles={["ADMIN", "CUSTOMER"]}>
              <OrdersPage />
            </ProtectedRoute>
          } />
          <Route path="orders/new" element={
            <ProtectedRoute allowedRoles={["ADMIN", "CUSTOMER"]}>
              <CreateOrderPage />
            </ProtectedRoute>
          } />
          <Route path="*" element={
            <div className="flex h-[50vh] flex-col items-center justify-center text-center">
              <h3 className="text-xl font-bold text-slate-800 dark:text-slate-200">Page Not Found</h3>
              <p className="text-sm text-slate-500 mt-1">The requested route does not exist.</p>
            </div>
          } />
        </Route>
      </Routes>
    </Router>
  )
}
