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
import { Plus, Search } from "lucide-react"
import usePagination from "../pagination/usePagination"
import Pagination from "../pagination/Pagination"
import ConfirmDialog from "../ui/ConfirmDialog"

export default function CustomersPage() {
  const dispatch = useDispatch()
  const { items, loading, error } = useSelector((state) => state.customers)
  
  const [searchQuery, setSearchQuery] = useState("")
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [deleteCustomerId, setDeleteCustomerId] = useState(null)

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

  const handleCreate = (data) => {
    const toastId = toast.loading("Adding customer...")
    dispatch(addCustomer(data)).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Customer added successfully", { id: toastId })
        setIsFormOpen(false)
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
    </div>
  )
}


