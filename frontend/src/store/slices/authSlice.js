import { createSlice } from "@reduxjs/toolkit"

const initialState = {
  accessToken: null,
  refreshToken: localStorage.getItem("refreshToken") || null,
  role: localStorage.getItem("userRole") || null,
  isAuthenticated: !!localStorage.getItem("refreshToken"),
  loading: false,
  error: null,
}

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    loginStart(state) {
      state.loading = true
      state.error = null
    },
    loginSuccess(state, action) {
      const { access_token, refresh_token, role } = action.payload
      state.loading = false
      state.accessToken = access_token
      state.refreshToken = refresh_token
      state.role = role
      state.isAuthenticated = true
      localStorage.setItem("refreshToken", refresh_token)
      localStorage.setItem("userRole", role)
    },
    loginFailure(state, action) {
      state.loading = false
      state.error = action.payload
    },
    tokenUpdate(state, action) {
      const { access_token, refresh_token } = action.payload
      state.accessToken = access_token
      state.refreshToken = refresh_token
      localStorage.setItem("refreshToken", refresh_token)
    },
    logout(state) {
      state.accessToken = null
      state.refreshToken = null
      state.role = null
      state.isAuthenticated = false
      state.loading = false
      state.error = null
      localStorage.removeItem("refreshToken")
      localStorage.removeItem("userRole")
    },
    clearError(state) {
      state.error = null
    }
  }
})

export const { 
  loginStart, 
  loginSuccess, 
  loginFailure, 
  tokenUpdate, 
  logout, 
  clearError 
} = authSlice.actions

export default authSlice.reducer
