import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { orderApi } from "../../api/client"

export const fetchOrders = createAsyncThunk(
  "orders/fetchAll",
  async ({ skip, limit } = { skip: 0, limit: 100 }, { rejectWithValue }) => {
    try {
      const response = await orderApi.list(skip, limit)
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

export const fetchOrderById = createAsyncThunk(
  "orders/fetchById",
  async (id, { rejectWithValue }) => {
    try {
      const response = await orderApi.get(id)
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

export const addOrder = createAsyncThunk(
  "orders/add",
  async (orderData, { rejectWithValue }) => {
    try {
      const response = await orderApi.create(orderData)
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

export const cancelOrder = createAsyncThunk(
  "orders/cancel",
  async (id, { rejectWithValue }) => {
    try {
      const response = await orderApi.cancel(id)
      return response.data // Should return the updated order structure with cancelled status
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

const orderSlice = createSlice({
  name: "orders",
  initialState: {
    items: [],
    currentOrder: null,
    loading: false,
    error: null,
  },
  reducers: {
    clearOrderError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Orders
      .addCase(fetchOrders.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchOrders.fulfilled, (state, action) => {
        state.loading = false
        state.items = action.payload
      })
      .addCase(fetchOrders.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      // Fetch Order By ID
      .addCase(fetchOrderById.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchOrderById.fulfilled, (state, action) => {
        state.loading = false
        state.currentOrder = action.payload
      })
      .addCase(fetchOrderById.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      // Add Order
      .addCase(addOrder.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(addOrder.fulfilled, (state, action) => {
        state.loading = false
        state.items.unshift(action.payload)
      })
      .addCase(addOrder.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      // Cancel Order
      .addCase(cancelOrder.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(cancelOrder.fulfilled, (state, action) => {
        state.loading = false
        const index = state.items.findIndex((o) => o.id === action.payload.id)
        if (index !== -1) {
          state.items[index] = action.payload
        }
        if (state.currentOrder && state.currentOrder.id === action.payload.id) {
          state.currentOrder = action.payload
        }
      })
      .addCase(cancelOrder.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  },
})

export const { clearOrderError } = orderSlice.actions
export default orderSlice.reducer
