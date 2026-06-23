import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { customerApi } from "../../api/client"

export const fetchCustomers = createAsyncThunk(
  "customers/fetchAll",
  async ({ skip, limit } = { skip: 0, limit: 100 }, { rejectWithValue }) => {
    try {
      const response = await customerApi.list(skip, limit)
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

export const addCustomer = createAsyncThunk(
  "customers/add",
  async (customerData, { rejectWithValue }) => {
    try {
      const response = await customerApi.create(customerData)
      return response.data
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

export const deleteCustomer = createAsyncThunk(
  "customers/delete",
  async (id, { rejectWithValue }) => {
    try {
      await customerApi.delete(id)
      return id
    } catch (error) {
      return rejectWithValue(error.message)
    }
  }
)

const customerSlice = createSlice({
  name: "customers",
  initialState: {
    items: [],
    loading: false,
    error: null,
  },
  reducers: {
    clearCustomerError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Customers
      .addCase(fetchCustomers.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.loading = false
        state.items = action.payload
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      // Add Customer
      .addCase(addCustomer.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(addCustomer.fulfilled, (state, action) => {
        state.loading = false
        state.items.unshift(action.payload)
      })
      .addCase(addCustomer.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      // Delete Customer
      .addCase(deleteCustomer.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(deleteCustomer.fulfilled, (state, action) => {
        state.loading = false
        state.items = state.items.filter((c) => c.id !== action.payload)
      })
      .addCase(deleteCustomer.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  },
})

export const { clearCustomerError } = customerSlice.actions
export default customerSlice.reducer
