import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import toast from "react-hot-toast"
import { 
  fetchCustomers, 
  addCustomer, 
  deleteCustomer, 
  clearCustomerError 
} from "../../store/slices/customerSlice"
import CustomerTable from "./CustomerTable"
import CustomerForm from "./CustomerForm"
import Breadcrumbs from "../ui/Breadcrumbs"
import { getErrorMessage } from "../../lib/errorMapper"
import { TableSkeleton } from "../ui/Skeleton"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import ConfirmDialog from "../ui/ConfirmDialog"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "../ui/dialog"
import { Plus, Search, Copy, Check, ShieldAlert } from "lucide-react"
import usePagination from "../pagination/usePagination"
import Pagination from "../pagination/Pagination"

export default function CustomersPage() {
  const dispatch = useDispatch()
  const { items, loading, error } = useSelector((state) => state.customers)
  
  const [searchQuery, setSearchQuery] = useState("")
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [deleteCustomerId, setDeleteCustomerId] = useState(null)
  const [registeredCustomer, setRegisteredCustomer] = useState(null)
  const [copied, setCopied] = useState(false)

  const filteredCustomers = items.filter((c) => {
    const fullName = `${c.first_name} ${c.last_name}`.toLowerCase()
    const email = c.email.toLowerCase()
    const query = searchQuery.toLowerCase()
    return fullName.includes(query) || email.includes(query)
  })

  const {
    currentPage,
    setCurrentPage,
    paginatedItems: paginatedCustomers,
    totalItems
  } = usePagination(filteredCustomers, 20)

  useEffect(() => {
    dispatch(fetchCustomers())
    return () => {
      dispatch(clearCustomerError())
    }
  }, [dispatch])

  // Toast notification for page-level/list loading errors
  useEffect(() => {
    if (error) {
      toast.error(getErrorMessage(error))
      dispatch(clearCustomerError())
    }
  }, [error, dispatch])

  // Reset pagination to page 1 when search query changes
  useEffect(() => {
    setCurrentPage(1)
  }, [searchQuery, setCurrentPage])

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    toast.success("Password copied to clipboard")
    setTimeout(() => setCopied(false), 2000)
  }

  const handleCreate = (data) => {
    const toastId = toast.loading("Adding customer...")
    dispatch(addCustomer(data)).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Customer added successfully", { id: toastId })
        setIsFormOpen(false)
        setRegisteredCustomer(action.payload)
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to add customer"), { id: toastId })
      }
    })
  }

  const handleDelete = (id) => {
    setDeleteCustomerId(id)
  }

  const executeDelete = () => {
    if (!deleteCustomerId) return
    const id = deleteCustomerId
    const toastId = toast.loading("Deleting customer...")
    dispatch(deleteCustomer(id)).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Customer deleted successfully", { id: toastId })
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to delete customer"), { id: toastId })
      }
    })
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <Breadcrumbs />
        </div>
        <Button
          onClick={() => setIsFormOpen(true)}
          className="bg-indigo-600 hover:bg-indigo-700 text-white flex items-center gap-1.5 self-start sm:self-auto text-xs font-semibold shadow-md shadow-indigo-100"
        >
          <Plus className="h-4 w-4" />
          <span>Add Customer</span>
        </Button>
      </div>

      {/* Search Filter */}
      <div className="flex items-center max-w-sm relative">
        <Search className="h-4 w-4 absolute left-3 text-slate-400" />
        <Input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search customers by name or email..."
          className="pl-9 text-xs"
        />
      </div>

      {/* Customer Registry Table */}
      {loading && items.length === 0 ? (
        <TableSkeleton cols={4} rows={5} />
      ) : (
        <>
          <CustomerTable customers={paginatedCustomers} onDelete={handleDelete} />
          <Pagination
            currentPage={currentPage}
            totalItems={totalItems}
            itemsPerPage={20}
            onPageChange={setCurrentPage}
          />
        </>
      )}

      {/* Form Modal Dialog */}
      <CustomerForm
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onSubmit={handleCreate}
      />

      {/* Confirm delete dialog */}
      <ConfirmDialog
        isOpen={deleteCustomerId !== null}
        onClose={() => setDeleteCustomerId(null)}
        onConfirm={executeDelete}
        title="Delete Customer"
        description="Are you sure you want to delete this customer? This action cannot be undone."
        confirmText="Delete"
        variant="destructive"
      />

      {/* Newly Registered Customer Info Dialog (shows temporary password) */}
      <Dialog open={registeredCustomer !== null} onOpenChange={(open) => !open && setRegisteredCustomer(null)}>
        <DialogContent className="sm:max-w-[420px] border border-slate-100 bg-white">
          <DialogHeader>
            <DialogTitle className="text-slate-800 font-bold flex items-center gap-2">
              Customer Registered
            </DialogTitle>
            <DialogDescription className="text-slate-500 text-xs mt-1.5 leading-relaxed">
              An account has been created for the customer. Please share their login credentials below.
            </DialogDescription>
          </DialogHeader>

          {registeredCustomer && (
            <div className="space-y-4 my-4 p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="space-y-1">
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">Full Name</span>
                <p className="text-sm font-semibold text-slate-700">
                  {registeredCustomer.first_name} {registeredCustomer.last_name}
                </p>
              </div>

              <div className="space-y-1">
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">Email Address</span>
                <p className="text-sm font-semibold text-slate-700">{registeredCustomer.email}</p>
              </div>

              {registeredCustomer.password && (
                <div className="space-y-2.5 pt-2 border-t border-slate-100">
                  <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400 flex items-center gap-1">
                    Temporary Password
                  </span>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm font-mono font-bold text-indigo-600 select-all">
                      {registeredCustomer.password}
                    </code>
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => copyToClipboard(registeredCustomer.password)}
                      className="h-9 w-9 text-slate-500 border-slate-200 hover:bg-slate-50 shrink-0"
                    >
                      {copied ? <Check className="h-4 w-4 text-emerald-500" /> : <Copy className="h-4 w-4" />}
                    </Button>
                  </div>
                  <div className="flex gap-1.5 items-start mt-1 text-[10px] text-amber-600 font-medium bg-amber-50/50 border border-amber-100/50 p-2 rounded-lg leading-relaxed">
                    <ShieldAlert className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>This password is only shown once. Make sure to copy it now before closing this window.</span>
                  </div>
                </div>
              )}
            </div>
          )}

          <DialogFooter className="mt-2">
            <Button
              onClick={() => setRegisteredCustomer(null)}
              className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-xs font-semibold text-white shadow-md shadow-indigo-100"
            >
              Done
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}


