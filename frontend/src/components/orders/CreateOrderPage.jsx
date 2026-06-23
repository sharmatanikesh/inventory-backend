import { useState, useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import toast from "react-hot-toast"
import { addOrder } from "../../store/slices/orderSlice"
import { fetchCustomers } from "../../store/slices/customerSlice"
import { fetchProducts } from "../../store/slices/productSlice"
import { getErrorMessage } from "../../lib/errorMapper"
import Breadcrumbs from "../ui/Breadcrumbs"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select"
import { Trash2, Plus, ArrowLeft } from "lucide-react"
import { CreateOrderSkeleton } from "../ui/Skeleton"

export default function CreateOrderPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const { items: customers, loading: customersLoading } = useSelector((state) => state.customers)
  const { items: products, loading: productsLoading } = useSelector((state) => state.products)

  const [customerId, setCustomerId] = useState("")
  const [items, setItems] = useState([{ product_id: "", quantity: 1 }])
  const [formError, setFormError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    dispatch(fetchCustomers())
    dispatch(fetchProducts())
  }, [dispatch])

  const isLoading = (customersLoading && customers.length === 0) || (productsLoading && products.length === 0)

  if (isLoading) {
    return <CreateOrderSkeleton />
  }

  const getProductInfo = (productId) => {
    return products.find((p) => p.id === productId) || null
  }

  const handleAddItem = () => {
    setItems([...items, { product_id: "", quantity: 1 }])
  }

  const handleRemoveItem = (index) => {
    const newItems = items.filter((_, i) => i !== index)
    setItems(newItems.length > 0 ? newItems : [{ product_id: "", quantity: 1 }])
  }

  const handleItemChange = (index, field, value) => {
    const newItems = [...items]
    newItems[index][field] = value
    setItems(newItems)
    setFormError("")
  }

  const calculateTotal = () => {
    return items.reduce((sum, item) => {
      const prod = getProductInfo(item.product_id)
      if (prod) {
        return sum + prod.price * (parseInt(item.quantity, 10) || 0)
      }
      return sum
    }, 0)
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!customerId) return setFormError("Please select a customer")

    const selectedProductIds = items.map((item) => item.product_id)
    const hasDuplicate = selectedProductIds.some((id, index) => selectedProductIds.indexOf(id) !== index)
    if (hasDuplicate) {
      return setFormError("Duplicate products selected. Adjust quantities instead.")
    }

    for (let i = 0; i < items.length; i++) {
      const item = items[i]
      if (!item.product_id) {
        return setFormError(`Please select a product for item line ${i + 1}`)
      }

      const qty = parseInt(item.quantity, 10)
      if (isNaN(qty) || qty <= 0) {
        return setFormError(`Quantity for item ${i + 1} must be greater than zero`)
      }

      const prod = getProductInfo(item.product_id)
      if (!prod) {
        return setFormError(`Product at item line ${i + 1} is invalid`)
      }

      if (qty > prod.quantity) {
        return setFormError(
          `Insufficient stock for "${prod.name}". Available stock: ${prod.quantity}. Requested: ${qty}`
        )
      }
    }

    setIsSubmitting(true)
    const toastId = toast.loading("Placing order...")

    dispatch(
      addOrder({
        customer_id: customerId,
        items: items.map((item) => ({
          product_id: item.product_id,
          quantity: parseInt(item.quantity, 10)
        }))
      })
    ).then((action) => {
      setIsSubmitting(false)
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Order placed successfully", { id: toastId })
        // Refresh products list since placing an order modifies stock
        dispatch(fetchProducts())
        navigate("/orders")
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to place order"), { id: toastId })
      }
    })
  }

  return (
    <div className="space-y-6">
      {/* Header and Breadcrumbs */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <Breadcrumbs />
        </div>
        <Button
          variant="outline"
          onClick={() => navigate("/orders")}
          className="flex items-center gap-1.5 self-start sm:self-auto text-xs font-semibold text-slate-600 border-slate-200 hover:bg-slate-50 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Orders</span>
        </Button>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left Section: Order Items Builder */}
        <div className="flex-1 rounded-lg border border-slate-100 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-50 pb-4 mb-5">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
              Order Items
            </h2>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={handleAddItem}
              className="h-8 px-3 text-xs font-bold flex items-center gap-1 text-indigo-600 border-indigo-100 hover:bg-indigo-50/50"
            >
              <Plus className="h-4 w-4" />
              <span>Add Item</span>
            </Button>
          </div>

          {formError && (
            <div className="rounded bg-rose-50 p-3 text-xs font-semibold text-rose-700 border border-rose-100 mb-4">
              {formError}
            </div>
          )}

          {/* List of item rows */}
          <div className="space-y-3.5">
            {items.map((item, index) => {
              const prod = getProductInfo(item.product_id)
              const isAvailable = prod ? prod.quantity : 0

              return (
                <div
                  key={index}
                  className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-start border border-slate-100 rounded-lg p-4 bg-slate-50/30"
                >
                  {/* Product drop down */}
                  <div className="flex-1 min-w-0 space-y-1">
                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                      Product {index + 1}
                    </label>
                    <Select
                      value={item.product_id}
                      onValueChange={(val) => handleItemChange(index, "product_id", val)}
                    >
                      <SelectTrigger className="w-full text-xs bg-white">
                        <SelectValue placeholder="Select product..." />
                      </SelectTrigger>
                      <SelectContent>
                        {products.map((p) => (
                          <SelectItem
                            key={p.id}
                            value={p.id}
                            disabled={p.quantity === 0}
                            className="text-xs"
                          >
                            {p.name} (${p.price.toFixed(2)}) — Stock: {p.quantity}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {prod && (
                      <span className="text-[10px] text-slate-400 block font-medium">
                        Stock level: {isAvailable} units remaining
                      </span>
                    )}
                  </div>

                  {/* Quantity input */}
                  <div className="w-full sm:w-28 space-y-1">
                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                      Quantity
                    </label>
                    <Input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) => handleItemChange(index, "quantity", e.target.value)}
                      placeholder="Qty"
                      required
                      className="text-xs bg-white h-10"
                    />
                  </div>

                  {/* Remove button */}
                  <div className="flex items-end justify-end sm:pt-5">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => handleRemoveItem(index)}
                      className="h-10 w-10 text-slate-400 hover:text-rose-600 transition-colors"
                    >
                      <Trash2 className="h-4.5 w-4.5" />
                    </Button>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Right Section: Customer & Total Panel */}
        <div className="w-full lg:w-96 space-y-6">
          {/* Customer selection card */}
          <div className="rounded-lg border border-slate-100 bg-white p-6 shadow-sm space-y-4">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider border-b border-slate-50 pb-3">
              Customer Info
            </h2>
            <div className="space-y-1.5">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                Select Customer
              </label>
              <Select value={customerId} onValueChange={setCustomerId}>
                <SelectTrigger className="w-full text-xs bg-white">
                  <SelectValue placeholder="Choose a customer..." />
                </SelectTrigger>
                <SelectContent>
                  {customers.map((c) => (
                    <SelectItem key={c.id} value={c.id} className="text-xs">
                      {c.first_name} {c.last_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Checkout pricing panel */}
          <div className="rounded-lg border border-slate-100 bg-white p-6 shadow-sm space-y-4">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider border-b border-slate-50 pb-3">
              Order Summary
            </h2>

            <div className="space-y-2">
              {items.map((item, idx) => {
                const prod = getProductInfo(item.product_id)
                if (!prod) return null
                const qty = parseInt(item.quantity, 10) || 0
                return (
                  <div key={idx} className="flex justify-between text-xs text-slate-500">
                    <span className="truncate max-w-[180px]">{prod.name} x {qty}</span>
                    <span className="font-semibold text-slate-700">${(prod.price * qty).toFixed(2)}</span>
                  </div>
                )
              })}
            </div>

            <div className="flex items-center justify-between border-t border-slate-50 pt-4 mt-2">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Amount:</span>
              <span className="text-xl font-black text-slate-800">
                ${calculateTotal().toFixed(2)}
              </span>
            </div>

            <div className="pt-2 space-y-2">
              <Button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold py-2.5 rounded-lg shadow-md shadow-indigo-100 disabled:opacity-50 transition-all duration-200"
              >
                {isSubmitting ? "Placing Order..." : "Place Order"}
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate("/orders")}
                className="w-full text-xs font-semibold border-slate-200 text-slate-500 hover:bg-slate-50 py-2.5 rounded-lg"
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
