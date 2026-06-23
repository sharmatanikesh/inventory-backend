import { useState, useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import { toast } from "react-hot-toast"
import { Lock, Mail, Loader2, ArrowRight } from "lucide-react"
import { authApi } from "../../api/client"
import { loginStart, loginSuccess, loginFailure, clearError } from "../../store/slices/authSlice"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { loading, error, isAuthenticated } = useSelector((state) => state.auth)

  useEffect(() => {
    // If already authenticated, redirect to home page
    if (isAuthenticated) {
      navigate("/")
    }
    return () => {
      dispatch(clearError())
    }
  }, [isAuthenticated, navigate, dispatch])

  const handleLogin = async (e) => {
    e.preventDefault()
    if (!email || !password) {
      toast.error("Please fill in all fields")
      return
    }

    dispatch(loginStart())
    try {
      const response = await authApi.login({ email, password })
      dispatch(loginSuccess(response.data))
      toast.success(response.message || "Logged in successfully!")
      navigate("/")
    } catch (err) {
      dispatch(loginFailure(err.message || "Failed to log in"))
      toast.error(err.message || "Invalid credentials")
    }
  }

  const fillCredentials = (type) => {
    if (type === "admin") {
      setEmail("admin@example.com")
      setPassword("admin1234")
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50/80 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 bg-white p-8 rounded-2xl border border-slate-100 shadow-xl shadow-slate-100/50">
        
        {/* Branding / Header */}
        <div className="text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-600 text-white font-extrabold text-lg shadow-md shadow-indigo-100">
            TS
          </div>
          <h2 className="mt-6 text-2xl font-black tracking-tight text-slate-800">
            Sign in to your account
          </h2>
          <p className="mt-2 text-xs text-slate-400 font-medium">
            Inventory & Order Management System
          </p>
        </div>

        {/* Login Form */}
        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          <div className="space-y-4 rounded-md">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <Mail className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full rounded-lg border border-slate-200 bg-slate-50/50 py-2.5 pl-10 pr-3 text-sm text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  placeholder="name@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1.5">
                Password
              </label>
              <div className="relative">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <Lock className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full rounded-lg border border-slate-200 bg-slate-50/50 py-2.5 pl-10 pr-3 text-sm text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  placeholder="••••••••"
                />
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative flex w-full items-center justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 transition-all duration-150"
            >
              {loading ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <>
                  Sign In
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                </>
              )}
            </button>
          </div>
        </form>

        {/* Demo Helper box */}
        <div className="mt-6 border-t border-slate-100 pt-6">
          <p className="text-xxs font-bold uppercase tracking-widest text-slate-400 text-center mb-3">
            Quick Fill Demo Account
          </p>
          <div className="flex justify-center">
            <button
              type="button"
              onClick={() => fillCredentials("admin")}
              className="w-full rounded-lg border border-slate-200/80 bg-white hover:bg-slate-50 px-3 py-2 text-xs font-semibold text-slate-600 shadow-sm transition-colors text-center"
            >
              Admin Staff Demo Account
            </button>
          </div>
        </div>


      </div>
    </div>
  )
}
