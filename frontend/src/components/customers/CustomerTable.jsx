import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table"
import { Button } from "../ui/button"
import { Trash2 } from "lucide-react"

export default function CustomerTable({ customers = [], onDelete }) {
  if (customers.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center border border-slate-100 rounded-lg bg-white shadow-sm">
        <p className="text-sm font-bold text-slate-500">No customers registered</p>
        <p className="text-xs text-slate-400 mt-1">Add a customer to start managing accounts</p>
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-slate-200/60 bg-white overflow-hidden shadow-sm">
      <Table className="min-w-[650px]">
        <TableHeader>
          <TableRow className="bg-slate-50/70 hover:bg-slate-50/70">
            <TableHead className="font-bold text-slate-500 text-xs">Full Name</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs">Email Address</TableHead>
            <TableHead className="font-bold text-slate-500 text-xs">Phone Number</TableHead>
            <TableHead className="text-right font-bold text-slate-500 text-xs">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {customers.map((customer) => (
            <TableRow key={customer.id} className="hover:bg-slate-50/30">
              <TableCell className="font-semibold text-slate-700 text-sm">
                {customer.first_name} {customer.last_name}
              </TableCell>
              <TableCell className="font-mono text-xs text-slate-500">
                {customer.email}
              </TableCell>
              <TableCell className="text-slate-500 text-sm">
                {customer.phone_number || "—"}
              </TableCell>
              <TableCell className="text-right">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onDelete(customer.id)}
                  className="h-8 w-8 text-slate-400 hover:text-rose-600 transition-colors"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
