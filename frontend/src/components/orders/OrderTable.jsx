import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table"
import { Button } from "../ui/button"
import { Eye, Ban } from "lucide-react"

export default function OrderTable({ orders = [], customers = [], onViewDetails, onCancel }) {
  const customerMap = customers.reduce((acc, c) => {
    acc[c.id] = `${c.first_name} ${c.last_name}`
    return acc
  }, {})

  if (orders.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center border border-slate-100 rounded-lg bg-white shadow-sm">
        <p className="text-sm font-bold text-slate-500">No orders found</p>
        <p className="text-xs text-slate-400 mt-1">Place an order to start recording transactions</p>
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-slate-200/60 bg-white overflow-hidden shadow-sm">
      <Table className="min-w-[900px]">
        <TableHeader>
          <TableRow className="bg-slate-50/70 hover:bg-slate-50/70">
            <TableHead className="font-bold text-slate-500 text-xs">Order ID</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs">Customer</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Total Amount</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs text-center">Status</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs text-center">Date</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs text-center">Time</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {orders.map((order) => {
            const customerName = customerMap[order.customer_id] || "Unknown Customer"
            const dateObj = new Date(order.created_at)
            const dateStr = dateObj.toLocaleDateString()
            const timeStr = dateObj.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
            const totalItems = order.items.reduce((acc, item) => acc + item.quantity, 0)
            const isCancelled = order.status === "CANCELLED" || order.status === "cancelled" || !!order.cancelled_at
            
            return (
              <TableRow key={order.id} className="hover:bg-slate-50/30">
                <TableCell className="font-mono text-xs text-slate-400">
                  {order.id.substring(0, 8)}
                </TableCell>
                <TableCell className="font-semibold text-slate-700 text-sm">
                  <div className="flex flex-col">
                    <span>{customerName}</span>
                    <span className="text-[10px] text-slate-400 font-normal mt-0.5">{totalItems} item(s)</span>
                  </div>
                </TableCell>
                <TableCell className="text-right font-bold text-slate-800 text-sm">
                  ${order.total_amount.toFixed(2)}
                </TableCell>
                <TableCell className="text-center">
                  <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[10px] font-bold ${
                    isCancelled
                      ? "bg-rose-50 text-rose-600 border border-rose-100"
                      : "bg-emerald-50 text-emerald-600 border border-emerald-100"
                  }`}>
                    {isCancelled ? "Cancelled" : "Completed"}
                  </span>
                </TableCell>
                <TableCell className="text-center text-xs text-slate-400 font-medium">
                  {dateStr}
                </TableCell>
                <TableCell className="text-center text-xs text-slate-400 font-medium">
                  {timeStr}
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => onViewDetails(order)}
                      title="View Order Details"
                      className="h-8 w-8 text-slate-400 hover:text-indigo-600 transition-colors"
                    >
                      <Eye className="h-3.5 w-3.5" />
                    </Button>
                    {!isCancelled && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => onCancel(order.id)}
                        title="Cancel Order"
                        className="h-8 w-8 text-slate-400 hover:text-rose-600 transition-colors"
                      >
                        <Ban className="h-3.5 w-3.5" />
                      </Button>
                    )}
                  </div>
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </div>
  )
}
