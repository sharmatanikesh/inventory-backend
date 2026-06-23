import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import toast from "react-hot-toast"
import { Link } from "react-router-dom"
import { 
  fetchOrders, 
  cancelOrder, 
  clearOrderError 
} from "../../store/slices/orderSlice"
import { fetchCustomers } from "../../store/slices/customerSlice"
import { fetchProducts } from "../../store/slices/productSlice"
import OrderTable from "./OrderTable"
import OrderDetailsDialog from "./OrderDetailsDialog"
import Breadcrumbs from "../ui/Breadcrumbs"
import { getErrorMessage } from "../../lib/errorMapper"
import { TableSkeleton } from "../ui/Skeleton"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Plus, Search } from "lucide-react"
import usePagination from "../pagination/usePagination"
import Pagination from "../pagination/Pagination"
import ConfirmDialog from "../ui/ConfirmDialog"

export default function OrdersPage() {
  const dispatch = useDispatch()
  
  // Select states from Redux slices
  const { items: orders, loading: ordersLoading, error: ordersError } = useSelector((state) => state.orders)
  const { items: customers } = useSelector((state) => state.customers)
  const { items: products } = useSelector((state) => state.products)

  const [searchQuery, setSearchQuery] = useState("")
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [isDetailsOpen, setIsDetailsOpen] = useState(false)
  const [cancelOrderId, setCancelOrderId] = useState(null)

  // Filter orders by customer name
  const filteredOrders = orders.filter((order) => {
    const customer = customers.find((c) => c.id === order.customer_id)
    const customerName = customer ? `${customer.first_name} ${customer.last_name}`.toLowerCase() : ""
    const orderId = order.id.toLowerCase()
    const query = searchQuery.toLowerCase()
    return customerName.includes(query) || orderId.includes(query)
  })

  const {
    currentPage,
    setCurrentPage,
    paginatedItems: paginatedOrders,
    totalItems
  } = usePagination(filteredOrders, 20)

  const loading = ordersLoading && orders.length === 0

  useEffect(() => {
    dispatch(fetchOrders())
    dispatch(fetchCustomers())
    dispatch(fetchProducts())
    return () => {
      dispatch(clearOrderError())
    }
  }, [dispatch])

  // Toast notification for page-level/list loading errors
  useEffect(() => {
    if (ordersError) {
      toast.error(getErrorMessage(ordersError))
      dispatch(clearOrderError())
    }
  }, [ordersError, dispatch])

  // Reset pagination to page 1 when search query changes
  useEffect(() => {
    setCurrentPage(1)
  }, [searchQuery, setCurrentPage])


  const handleCancel = (id) => {
    setCancelOrderId(id)
  }

  const executeCancel = () => {
    if (!cancelOrderId) return
    const id = cancelOrderId
    const toastId = toast.loading("Cancelling order...")
    dispatch(cancelOrder(id)).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Order cancelled and restocked successfully", { id: toastId })
        // Refresh products list since cancelling an order restores stock
        dispatch(fetchProducts())
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to cancel order"), { id: toastId })
      }
    })
  }


  const handleViewDetails = (order) => {
    setSelectedOrder(order)
    setIsDetailsOpen(true)
  }

  const handleCloseDetails = () => {
    setIsDetailsOpen(false)
    setSelectedOrder(null)
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <Breadcrumbs />
        </div>
        <Link to="/orders/new">
          <Button
            className="bg-indigo-600 hover:bg-indigo-700 text-white flex items-center gap-1.5 self-start sm:self-auto"
          >
            <Plus className="h-4 w-4" />
            <span>New Order</span>
          </Button>
        </Link>
      </div>

      {/* Search Filter */}
      <div className="flex items-center max-w-sm relative">
        <Search className="h-4 w-4 absolute left-3 text-slate-400" />
        <Input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search orders by customer or ID..."
          className="pl-9"
        />
      </div>

      {/* Orders Grid Table */}
      {loading ? (
        <TableSkeleton cols={6} rows={5} />
      ) : (
        <>
          <OrderTable
            orders={paginatedOrders}
            customers={customers}
            onViewDetails={handleViewDetails}
            onCancel={handleCancel}
          />
          <Pagination
            currentPage={currentPage}
            totalItems={totalItems}
            itemsPerPage={20}
            onPageChange={setCurrentPage}
          />
        </>
      )}

      {/* Invoice details viewer modal */}
      <OrderDetailsDialog
        order={selectedOrder}
        isOpen={isDetailsOpen}
        onClose={handleCloseDetails}
        customers={customers}
        products={products}
      />

      {/* Confirm cancel dialog */}
      <ConfirmDialog
        isOpen={cancelOrderId !== null}
        onClose={() => setCancelOrderId(null)}
        onConfirm={executeCancel}
        title="Cancel Order"
        description="Are you sure you want to cancel this order? This will restock the order items and cannot be undone."
        confirmText="Yes, cancel order"
        variant="destructive"
      />
    </div>
  )
}



