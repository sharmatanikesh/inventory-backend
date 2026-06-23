import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table"
import { AlertTriangle, ShieldCheck } from "lucide-react"

export default function LowStockAlerts({ items = [] }) {
  return (
    <Card className="col-span-1 md:col-span-2 border border-slate-100 bg-white">
      <CardHeader className="flex flex-row items-center justify-between pb-3">
        <div>
          <CardTitle className="text-base font-bold text-slate-800">Low Stock Alerts</CardTitle>
          <CardDescription className="text-xs text-slate-400">Products requiring immediate restocking</CardDescription>
        </div>
        {items.length > 0 ? (
          <div className="flex items-center gap-1.5 rounded-full bg-amber-50 px-2.5 py-1 text-[11px] font-semibold text-amber-700 border border-amber-100">
            <AlertTriangle className="h-3 w-3" />
            <span>{items.length} Warning(s)</span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5 rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-semibold text-emerald-700 border border-emerald-100">
            <ShieldCheck className="h-3 w-3" />
            <span>Stock Healthy</span>
          </div>
        )}
      </CardHeader>
      <CardContent>
        {items.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <p className="text-xs font-semibold text-slate-400">
              All product stock levels are above the warning threshold.
            </p>
          </div>
        ) : (
          <div className="relative overflow-x-auto rounded-lg border border-slate-100">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-50/70 hover:bg-slate-50/70">
                  <TableHead className="w-[100px] font-bold text-slate-500 text-xs">SKU / ID</TableHead>
                  <TableHead className="font-bold text-slate-500 text-xs">Product Name</TableHead>
                  <TableHead className="text-right font-bold text-slate-500 text-xs">Quantity Left</TableHead>
                  <TableHead className="text-right font-bold text-slate-500 text-xs">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {items.map((product) => (
                  <TableRow key={product.id} className="hover:bg-slate-50/30">
                    <TableCell className="font-mono text-xs text-slate-400">
                      {product.id.substring(0, 8)}
                    </TableCell>
                    <TableCell className="font-semibold text-slate-700 text-sm">
                      {product.name}
                    </TableCell>
                    <TableCell className="text-right font-bold text-slate-800 text-sm">
                      {product.quantity}
                    </TableCell>
                    <TableCell className="text-right">
                      <span className={`inline-flex rounded-full px-2 py-0.5 text-[10px] font-bold ${
                        product.quantity === 0
                          ? "bg-rose-50 text-rose-600 border border-rose-100"
                          : "bg-amber-50 text-amber-600 border border-amber-100"
                      }`}>
                        {product.quantity === 0 ? "Out of Stock" : "Low Stock"}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
