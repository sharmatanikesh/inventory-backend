import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import toast from "react-hot-toast"
import { 
  fetchProducts, 
  addProduct, 
  updateProduct, 
  deleteProduct,
  clearProductError
} from "../../store/slices/productSlice"
import ProductTable from "./ProductTable"
import ProductForm from "./ProductForm"
import Breadcrumbs from "../ui/Breadcrumbs"
import { getErrorMessage } from "../../lib/errorMapper"
import { TableSkeleton } from "../ui/Skeleton"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Plus, Search } from "lucide-react"
import usePagination from "../pagination/usePagination"
import Pagination from "../pagination/Pagination"
import ConfirmDialog from "../ui/ConfirmDialog"

export default function ProductsPage() {
  const dispatch = useDispatch()
  const { items, loading, error } = useSelector((state) => state.products)
  
  const [searchQuery, setSearchQuery] = useState("")
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [deleteProductId, setDeleteProductId] = useState(null)

  const filteredProducts = items.filter(
    (p) =>
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.sku.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const {
    currentPage,
    setCurrentPage,
    paginatedItems: paginatedProducts,
    totalItems
  } = usePagination(filteredProducts, 20)

  useEffect(() => {
    dispatch(fetchProducts())
    return () => {
      dispatch(clearProductError())
    }
  }, [dispatch])

  // Toast notification for page-level/list loading errors
  useEffect(() => {
    if (error) {
      toast.error(getErrorMessage(error))
      dispatch(clearProductError())
    }
  }, [error, dispatch])

  // Reset pagination to page 1 when search query changes
  useEffect(() => {
    setCurrentPage(1)
  }, [searchQuery, setCurrentPage])

  const handleCreate = (data) => {
    const toastId = toast.loading("Creating product...")
    dispatch(addProduct(data)).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Product created successfully", { id: toastId })
        setIsFormOpen(false)
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to create product"), { id: toastId })
      }
    })
  }

  const handleUpdate = (data) => {
    const toastId = toast.loading("Updating product...")
    dispatch(updateProduct({ id: editingProduct.id, data })).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Product updated successfully", { id: toastId })
        setIsFormOpen(false)
        setEditingProduct(null)
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to update product"), { id: toastId })
      }
    })
  }

  const handleDelete = (id) => {
    setDeleteProductId(id)
  }

  const executeDelete = () => {
    if (!deleteProductId) return
    const id = deleteProductId
    const toastId = toast.loading("Deleting product...")
    dispatch(deleteProduct(id)).then((action) => {
      if (action.meta.requestStatus === "fulfilled") {
        toast.success("Product deleted successfully", { id: toastId })
      } else {
        toast.error(getErrorMessage(action.payload || "Failed to delete product"), { id: toastId })
      }
    })
  }

  const handleEditClick = (product) => {
    setEditingProduct(product)
    setIsFormOpen(true)
  }

  const handleCloseForm = () => {
    setIsFormOpen(false)
    setEditingProduct(null)
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
          <span>Add Product</span>
        </Button>
      </div>

      {/* Search Filter */}
      <div className="flex items-center max-w-sm relative">
        <Search className="h-4 w-4 absolute left-3 text-slate-400" />
        <Input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search products by name or SKU..."
          className="pl-9 text-xs"
        />
      </div>

      {/* Product Table List */}
      {loading && items.length === 0 ? (
        <TableSkeleton cols={6} rows={5} />
      ) : (
        <>
          <ProductTable
            products={paginatedProducts}
            onEdit={handleEditClick}
            onDelete={handleDelete}
          />
          <Pagination
            currentPage={currentPage}
            totalItems={totalItems}
            itemsPerPage={20}
            onPageChange={setCurrentPage}
          />
        </>
      )}

      {/* Product Form Modal */}
      <ProductForm
        isOpen={isFormOpen}
        onClose={handleCloseForm}
        onSubmit={editingProduct ? handleUpdate : handleCreate}
        initialData={editingProduct}
      />

      {/* Confirm delete dialog */}
      <ConfirmDialog
        isOpen={deleteProductId !== null}
        onClose={() => setDeleteProductId(null)}
        onConfirm={executeDelete}
        title="Delete Product"
        description="Are you sure you want to delete this product? This action cannot be undone."
        confirmText="Delete"
        variant="destructive"
      />
    </div>
  )
}


