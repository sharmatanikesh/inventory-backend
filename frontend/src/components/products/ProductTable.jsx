import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table"
import { Button } from "../ui/button"
import { Edit2, Trash2 } from "lucide-react"

export default function ProductTable({ products = [], onEdit, onDelete }) {
  if (products.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center border border-slate-100 rounded-lg bg-white shadow-sm">
        <p className="text-sm font-bold text-slate-500">No products found</p>
        <p className="text-xs text-slate-400 mt-1">Add a product to start tracking your inventory</p>
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-slate-200/60 bg-white overflow-hidden shadow-sm">
      <Table className="min-w-[800px]">
        <TableHeader>
          <TableRow className="bg-slate-50/70 hover:bg-slate-50/70">
            <TableHead className="font-bold text-slate-500 text-xs">SKU</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs">Product Name</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Price</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Quantity</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Status</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {products.map((product) => {
            const isLowStock = product.quantity <= 5
            const isOutOfStock = product.quantity === 0
            
            return (
              <TableRow key={product.id} className="hover:bg-slate-50/30">
                <TableCell className="font-mono text-xs font-bold text-indigo-600">
                  {product.sku}
                </TableCell>
                <TableCell className="font-semibold text-slate-700 text-sm">
                  {product.name}
                </TableCell>
                <TableCell className="text-right font-bold text-slate-800 text-sm">
                  ${product.price.toFixed(2)}
                </TableCell>
                <TableCell className="text-right font-bold text-slate-800 text-sm">
                  {product.quantity}
                </TableCell>
                <TableCell className="text-right">
                  <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[10px] font-bold ${
                    isOutOfStock
                      ? "bg-rose-50 text-rose-600 border border-rose-100"
                      : isLowStock
                      ? "bg-amber-50 text-amber-600 border border-amber-100"
                      : "bg-emerald-50 text-emerald-600 border border-emerald-100"
                  }`}>
                    {isOutOfStock ? "Out of Stock" : isLowStock ? "Low Stock" : "In Stock"}
                  </span>
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => onEdit(product)}
                      className="h-8 w-8 text-slate-400 hover:text-indigo-600 transition-colors"
                    >
                      <Edit2 className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => onDelete(product.id)}
                      className="h-8 w-8 text-slate-400 hover:text-rose-600 transition-colors"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
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
