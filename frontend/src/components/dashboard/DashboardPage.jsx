import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import toast from "react-hot-toast"
import { fetchDashboardSummary, clearDashboardError } from "../../store/slices/dashboardSlice"
import StatsOverview from "./StatsOverview"
import LowStockAlerts from "./LowStockAlerts"
import Breadcrumbs from "../ui/Breadcrumbs"
import { getErrorMessage } from "../../lib/errorMapper"
import { RefreshCw } from "lucide-react"
import { DashboardSkeleton } from "../ui/Skeleton"

export default function DashboardPage() {
  const dispatch = useDispatch()
  const { summary, loading, error } = useSelector((state) => state.dashboard)

  useEffect(() => {
    dispatch(fetchDashboardSummary())
    return () => {
      dispatch(clearDashboardError())
    }
  }, [dispatch])

  // Toast notification for dashboard loading errors
  useEffect(() => {
    if (error) {
      toast.error(getErrorMessage(error))
      dispatch(clearDashboardError())
    }
  }, [error, dispatch])

  const handleRefresh = () => {
    dispatch(fetchDashboardSummary())
  }

  if (loading && !summary) {
    return <DashboardSkeleton />
  }

  return (
    <div className="space-y-8">
      {/* Title Header */}
      <div className="flex items-center justify-between">
        <div>
          <Breadcrumbs />
        </div>
        <button
          onClick={handleRefresh}
          disabled={loading}
          className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 disabled:opacity-50 transition-colors shadow-sm"
        >
          <RefreshCw className={`h-3 w-3 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh</span>
        </button>
      </div>

      {summary && (
        <>
          {/* Stats overview cards */}
          <StatsOverview
            totalProducts={summary.total_products}
            totalCustomers={summary.total_customers}
            totalOrders={summary.total_orders}
          />

          {/* Low stock table section */}
          <LowStockAlerts items={summary.low_stock_products} />
        </>
      )}
    </div>
  )
}
