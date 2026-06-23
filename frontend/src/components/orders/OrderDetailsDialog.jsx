import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "../ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table"
import { Button } from "../ui/button"

export default function OrderDetailsDialog({ order, isOpen, onClose, customers = [], products = [] }) {
  if (!order) return null

  // Find customer name
  const customer = customers.find((c) => c.id === order.customer_id)
  const customerName = customer ? `${customer.first_name} ${customer.last_name}` : "Unknown Customer"
  const customerEmail = customer ? customer.email : "—"

  // Helper to get product details
  const getProductDetails = (productId) => {
    const product = products.find((p) => p.id === productId)
    return product ? { name: product.name, sku: product.sku } : { name: "Unknown Product", sku: "N/A" }
  }

  const isCancelled = order.status === "CANCELLED" || order.status === "cancelled" || !!order.cancelled_at

  return (
    <Dialog open={isOpen} onOpenChange={(val) => !val && onClose()}>
      <DialogContent className="sm:max-w-[550px] max-h-[85vh] overflow-y-auto border border-slate-100 bg-white">
        <DialogHeader>
          <DialogTitle className="text-lg font-bold text-slate-800 flex items-center justify-between pr-4">
            <span>Order Invoice</span>
            <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[10px] font-bold ${
              isCancelled
                ? "bg-rose-50 text-rose-600 border border-rose-100"
                : "bg-emerald-50 text-emerald-600 border border-emerald-100"
            }`}>
              {isCancelled ? "Cancelled" : "Completed"}
            </span>
          </DialogTitle>
        </DialogHeader>

        {/* Invoice Body */}
        <div className="space-y-6 py-2">
          {/* Metadata Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 rounded-lg bg-slate-50 p-4 text-xs border border-slate-100">
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Order Information</p>
              <p className="text-slate-600">
                <span className="font-semibold text-slate-500">ID: </span>
                <span className="font-mono text-[11px]">{order.id}</span>
              </p>
              <p className="text-slate-600 mt-1">
                <span className="font-semibold text-slate-500">Date: </span>
                {new Date(order.created_at).toLocaleString()}
              </p>
              {order.cancelled_at && (
                <p className="text-rose-600 font-bold mt-1">
                  <span>Cancelled At: </span>
                  {new Date(order.cancelled_at).toLocaleString()}
                </p>
              )}
            </div>

            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Customer Details</p>
              <p className="font-bold text-slate-700">{customerName}</p>
              <p className="text-[11px] text-slate-400 font-mono mt-0.5">{customerEmail}</p>
              {customer?.phone_number && (
                <p className="text-[11px] text-slate-500 mt-0.5">{customer.phone_number}</p>
              )}
            </div>
          </div>

          {/* Items Table */}
          <div className="space-y-2">
            <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Ordered Items</h4>
            <div className="rounded-lg border border-slate-100 overflow-hidden shadow-sm">
              <Table className="min-w-[500px]">
                <TableHeader>
                  <TableRow className="bg-slate-50/70 hover:bg-slate-50/70">
                    <TableHead className="font-bold text-slate-500 text-xs">Product</TableHead>
                    <TableHead className="text-right font-bold text-slate-500 text-xs">Price</TableHead>
                    <TableHead className="text-right font-bold text-slate-500 text-xs">Qty</TableHead>
                    <TableHead className="text-right font-bold text-slate-500 text-xs">Total</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {order.items.map((item) => {
                    const prodInfo = getProductDetails(item.product_id)
                    const itemTotal = item.unit_price * item.quantity
                    return (
                      <TableRow key={item.id} className="hover:bg-slate-50/30">
                        <TableCell>
                          <div className="flex flex-col">
                            <span className="font-semibold text-slate-700 text-sm">{prodInfo.name}</span>
                            <span className="font-mono text-[10px] text-slate-400 mt-0.5">{prodInfo.sku}</span>
                          </div>
                        </TableCell>
                        <TableCell className="text-right text-slate-600 text-sm">${item.unit_price.toFixed(2)}</TableCell>
                        <TableCell className="text-right font-bold text-slate-700 text-sm">{item.quantity}</TableCell>
                        <TableCell className="text-right font-bold text-slate-800 text-sm">
                          ${itemTotal.toFixed(2)}
                        </TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* Total Summary */}
          <div className="flex justify-end text-right">
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Grand Total</span>
              <div className="text-xl font-black text-slate-800">
                ${order.total_amount.toFixed(2)}
              </div>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button onClick={onClose} className="bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold">
            Close Invoice
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
