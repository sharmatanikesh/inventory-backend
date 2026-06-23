import { Link, useLocation } from "react-router-dom"
import { useSelector } from "react-redux"
import { 
  LayoutDashboard, 
  Package, 
  Users, 
  ShoppingCart,
  ChevronLeft,
  ChevronRight
} from "lucide-react"

export default function Sidebar({ isOpen, setIsOpen }) {
  const location = useLocation()
  const role = useSelector((state) => state.auth.role)

  const menuItems = [
    { name: "Dashboard", path: "/", icon: LayoutDashboard, roles: ["ADMIN"] },
    { name: "Products", path: "/products", icon: Package, roles: ["ADMIN"] },
    { name: "Customers", path: "/customers", icon: Users, roles: ["ADMIN"] },
    { name: "Orders", path: "/orders", icon: ShoppingCart, roles: ["ADMIN", "CUSTOMER"] },
  ]

  const filteredMenuItems = menuItems.filter(item => item.roles.includes(role))

  const handleLinkClick = () => {
    if (window.innerWidth < 768) {
      setIsOpen(false)
    }
  }

  return (
    <aside
      className={`fixed inset-y-0 left-0 z-30 flex flex-col border-r border-slate-100 bg-white transition-all duration-300 ${
        isOpen 
          ? "translate-x-0 w-64" 
          : "-translate-x-full md:translate-x-0 md:w-20"
      } ${isOpen ? "md:w-64" : ""}`}
    >
      {/* Sidebar Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-slate-100">
        <Link to="/" onClick={handleLinkClick} className="flex items-center gap-2 font-bold text-slate-900">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 text-white font-extrabold text-xs shadow-md shadow-indigo-100">
            TS
          </div>
          {isOpen && <span className="text-base tracking-tight font-extrabold text-slate-800">Inventory</span>}
        </Link>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="hidden md:flex h-6 w-6 items-center justify-center rounded-full border border-slate-200 bg-white hover:bg-slate-50 text-slate-400 hover:text-slate-700 transition-colors shadow-sm"
        >
          {isOpen ? <ChevronLeft className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 space-y-1.5 px-3 py-5">
        {filteredMenuItems.map((item) => {
          const isActive = location.pathname === item.path
          const Icon = item.icon
          return (
            <Link
              key={item.name}
              to={item.path}
              onClick={handleLinkClick}
              className={`group flex items-center gap-3 rounded-lg px-3.5 py-2.5 text-xs font-semibold tracking-wide uppercase transition-all duration-200 ${
                isActive
                  ? "bg-indigo-50/80 text-indigo-600 shadow-sm"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <Icon className={`h-4.5 w-4.5 transition-transform duration-200 group-hover:scale-105 ${isActive ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-500"}`} />
              {isOpen && <span>{item.name}</span>}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
