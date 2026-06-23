import axios from "axios"
import { store } from "../store"
import { tokenUpdate, logout } from "../store/slices/authSlice"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: {
    "Content-Type": "application/json",
  },
})

// Attach Access Token to request headers
api.interceptors.request.use(
  (config) => {
    const token = store.getState().auth.accessToken
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor with automatic token refresh on 401
api.interceptors.response.use(
  (response) => {
    // If response is wrapped in standard APIResponse wrapper
    if (response.data && typeof response.data === "object" && "success" in response.data) {
      if (response.data.success) {
        return response.data; // Return the full envelope
      } else {
        return Promise.reject(new Error(response.data.message || "Operation failed"))
      }
    }
    return response.data
  },
  async (error) => {
    const originalRequest = error.config
    
    // Avoid infinite refresh loop by checking _retry flag
    // Also skip refresh token request on login/refresh/logout routes
    const isAuthRoute = originalRequest.url.includes("/auth/")

    if (error.response?.status === 401 && !originalRequest._retry && !isAuthRoute) {
      originalRequest._retry = true
      const state = store.getState()
      const refreshToken = state.auth.refreshToken || localStorage.getItem("refreshToken")

      if (refreshToken) {
        try {
          // Use a clean axios instance to refresh to avoid triggers
          const refreshResponse = await axios.post(
            `${api.defaults.baseURL}/auth/refresh`,
            { refresh_token: refreshToken },
            { headers: { "Content-Type": "application/json" } }
          )

          if (refreshResponse.data && refreshResponse.data.success) {
            const { access_token, refresh_token } = refreshResponse.data.data
            
            // Update Redux state and local storage
            store.dispatch(tokenUpdate({ access_token, refresh_token }))
            
            // Retry the original request with new token
            originalRequest.headers.Authorization = `Bearer ${access_token}`
            return api(originalRequest)
          }
        } catch (refreshError) {
          // If refresh token has expired or is invalid, force logout
          store.dispatch(logout())
          window.location.href = "/login"
          return Promise.reject(new Error("Session expired. Please login again."))
        }
      }
    }

    let errorMessage = "An unexpected error occurred."
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        if (typeof error.response.data.detail === "string") {
          errorMessage = error.response.data.detail
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map((err) => `${err.loc.join(".")}: ${err.msg}`).join("; ")
        }
      } else if (error.response.data.message) {
        errorMessage = error.response.data.message
      }
    } else if (error.message) {
      errorMessage = error.message
    }
    return Promise.reject(new Error(errorMessage))
  }
)

export const authApi = {
  login: (data) => api.post("/auth/login", data),
  refresh: (data) => api.post("/auth/refresh", data),
  logout: (data) => {
    const refreshToken = store.getState().auth.refreshToken || localStorage.getItem("refreshToken")
    return api.post("/auth/logout", { refresh_token: refreshToken })
  },
}

export const dashboardApi = {
  getSummary: () => api.get("/dashboard/summary"),
}

export const productApi = {
  list: (skip = 0, limit = 100) => api.get(`/products/?skip=${skip}&limit=${limit}`),
  get: (id) => api.get(`/products/${id}`),
  create: (data) => api.post("/products/", data),
  update: (id, data) => api.put(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`),
}

export const customerApi = {
  list: (skip = 0, limit = 100) => api.get(`/customers/?skip=${skip}&limit=${limit}`),
  get: (id) => api.get(`/customers/${id}`),
  create: (data) => api.post("/customers/", data),
  delete: (id) => api.delete(`/customers/${id}`),
}

export const orderApi = {
  list: (skip = 0, limit = 100) => api.get(`/orders/?skip=${skip}&limit=${limit}`),
  get: (id) => api.get(`/orders/${id}`),
  create: (data) => api.post("/orders/", data),
  cancel: (id) => api.delete(`/orders/${id}`),
}

export default api
