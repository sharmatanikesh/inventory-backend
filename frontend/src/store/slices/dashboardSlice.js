import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { dashboardApi } from "../../api/client"

export const fetchDashboardSummary = createAsyncThunk(
  "dashboard/fetchSummary",
  async (_, { rejectWithValue }) => {
    try {
      const response = await dashboardApi.getSummary()
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState: {
    summary: null,
    loading: false,
    error: null,
  },
  reducers: {
    clearDashboardError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardSummary.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchDashboardSummary.fulfilled, (state, action) => {
        state.loading = false
        state.summary = action.payload
      })
      .addCase(fetchDashboardSummary.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  },
})

export const { clearDashboardError } = dashboardSlice.actions
export default dashboardSlice.reducer
