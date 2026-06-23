import { useLocation, Link } from "react-router-dom"
import { ChevronRight, Home } from "lucide-react"

export default function Breadcrumbs() {
  const location = useLocation()
  const pathnames = location.pathname.split("/").filter((x) => x)

  const getBreadcrumbs = () => {
    const breadcrumbs = [
      { label: "Home", path: "/", isLast: pathnames.length === 0 }
    ]
    
    pathnames.forEach((value, index) => {
      const path = `/${pathnames.slice(0, index + 1).join("/")}`
      const label = value.charAt(0).toUpperCase() + value.slice(1)
      breadcrumbs.push({
        label,
        path,
        isLast: index === pathnames.length - 1
      })
    })
    
    return breadcrumbs
  }

  return (
    <nav className="flex flex-wrap items-center gap-y-1 space-x-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
      {getBreadcrumbs().map((bc, idx) => (
        <div key={bc.path} className="flex items-center space-x-1">
          {idx > 0 && <ChevronRight className="h-3 w-3 text-slate-300" />}
          {bc.isLast ? (
            <span className="text-slate-500 font-bold">{bc.label}</span>
          ) : (
            <Link
              to={bc.path}
              className="hover:text-indigo-600 text-slate-400 transition-colors flex items-center gap-0.5"
            >
              {idx === 0 && <Home className="h-3 w-3 text-slate-400" />}
              <span>{bc.label}</span>
            </Link>
          )}
        </div>
      ))}
    </nav>
  )
}
