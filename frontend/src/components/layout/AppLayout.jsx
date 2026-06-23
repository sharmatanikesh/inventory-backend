import { useState, useEffect } from "react"
import { Outlet, useNavigate } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux"
import { toast } from "react-hot-toast"
import Sidebar from "./Sidebar"
import { Menu, LogOut } from "lucide-react"
import { authApi } from "../../api/client"
import { logout } from "../../store/slices/authSlice"

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const role = useSelector((state) => state.auth.role)

  useEffect(() => {
    if (window.innerWidth >= 768) {
      setSidebarOpen(true)
    }
  }, [])

  const handleLogout = async () => {
    try {
      // Call logout API to revoke session on server
      await authApi.logout()
    } catch (err) {
      // Ignore API failure for clean client state reset
    }
    dispatch(logout())
    toast.success("Logged out successfully")
    navigate("/login")
  }

  return (
    <div className="min-h-screen bg-slate-50/80 text-slate-900 transition-colors duration-300">
      {/* Mobile Sidebar Overlay Backdrop */}
      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 z-20 bg-slate-950/40 backdrop-blur-sm md:hidden transition-opacity duration-300 cursor-pointer"
        />
      )}

      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

      {/* Main Content Area */}
      <div
        className={`flex flex-col min-h-screen transition-all duration-300 ${
          sidebarOpen ? "md:pl-64" : "md:pl-20"
        }`}
      >
        {/* Header / Navbar */}
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-100 bg-white/90 px-6 backdrop-blur-md shadow-sm">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="md:hidden flex h-10 w-10 items-center justify-center rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-500"
            >
              <Menu className="h-5 w-5" />
            </button>
            
            <h2 className="text-lg font-bold tracking-tight text-slate-800">
              Inventory
            </h2>
          </div>

          {/* User Profile & Logout Action */}
          <div className="flex items-center gap-4">
            {role && (
              <div className="hidden sm:flex flex-col text-right">
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">Signed in as</span>
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">{role}</span>
              </div>
            )}
            
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 rounded-lg border border-slate-200/80 bg-white hover:bg-rose-50 hover:border-rose-100 hover:text-rose-600 px-3.5 py-2 text-xs font-bold text-slate-500 shadow-sm transition-all duration-150"
            >
              <LogOut className="h-3.5 w-3.5" />
              Logout
            </button>
          </div>
        </header>

        {/* Page Body Container */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto animate-fadeIn">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
