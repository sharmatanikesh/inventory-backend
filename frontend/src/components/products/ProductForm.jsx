import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "../ui/dialog"
import { Button } from "../ui/button"
import { Input } from "../ui/input"

export default function ProductForm({ isOpen, onClose, onSubmit, initialData = null }) {
  const [name, setName] = useState("")
  const [sku, setSku] = useState("")
  const [price, setPrice] = useState("")
  const [quantity, setQuantity] = useState("")
  const [formError, setFormError] = useState("")

  useEffect(() => {
    if (initialData) {
      setName(initialData.name)
      setSku(initialData.sku)
      setPrice(initialData.price.toString())
      setQuantity(initialData.quantity.toString())
    } else {
      setName("")
      setSku("")
      setPrice("")
      setQuantity("")
    }
    setFormError("")
  }, [initialData, isOpen])

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!name.trim()) return setFormError("Product name is required")
    if (!sku.trim()) return setFormError("SKU code is required")
    
    const parsedPrice = parseFloat(price)
    if (isNaN(parsedPrice) || parsedPrice <= 0) {
      return setFormError("Price must be a positive number")
    }

    const parsedQuantity = parseInt(quantity, 10)
    if (isNaN(parsedQuantity) || parsedQuantity < 0) {
      return setFormError("Quantity cannot be negative")
    }

    onSubmit({
      name: name.trim(),
      sku: sku.trim().toUpperCase(),
      price: parsedPrice,
      quantity: parsedQuantity,
    })
  }

  return (
    <Dialog open={isOpen} onOpenChange={(val) => !val && onClose()}>
      <DialogContent className="sm:max-w-[400px] border border-slate-100 bg-white">
        <DialogHeader>
          <DialogTitle className="text-lg font-bold text-slate-800">
            {initialData ? "Edit Product" : "Add Product"}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 py-2">
          {formError && (
            <div className="rounded bg-rose-50 p-2.5 text-xs font-semibold text-rose-700 border border-rose-100">
              {formError}
            </div>
          )}

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Product Name
            </label>
            <Input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Wireless Mouse"
              required
              className="text-sm"
            />
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              SKU Code
            </label>
            <Input
              value={sku}
              onChange={(e) => setSku(e.target.value)}
              placeholder="e.g. MOUSE-WRLS-001"
              required
              disabled={!!initialData}
              className="text-sm font-mono uppercase"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                Price ($)
              </label>
              <Input
                type="number"
                step="0.01"
                min="0.01"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                placeholder="0.00"
                required
                className="text-sm"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                Quantity
              </label>
              <Input
                type="number"
                min="0"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="0"
                required
                className="text-sm"
              />
            </div>
          </div>

          <DialogFooter className="pt-4 flex gap-2">
            <Button type="button" variant="outline" onClick={onClose} className="text-xs font-semibold">
              Cancel
            </Button>
            <Button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-md shadow-indigo-100">
              {initialData ? "Save Changes" : "Create Product"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
