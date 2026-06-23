import { configureStore } from "@reduxjs/toolkit"
import productReducer from "./slices/productSlice"
import customerReducer from "./slices/customerSlice"
import orderReducer from "./slices/orderSlice"
import dashboardReducer from "./slices/dashboardSlice"
import authReducer from "./slices/authSlice"

export const store = configureStore({
  reducer: {
    products: productReducer,
    customers: customerReducer,
    orders: orderReducer,
    dashboard: dashboardReducer,
    auth: authReducer,
  },
})


export default store
