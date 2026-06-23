import React from "react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "./dialog"
import { Button } from "./button"

export default function ConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  title = "Confirm Action",
  description = "Are you sure you want to perform this action?",
  confirmText = "Confirm",
  cancelText = "Cancel",
  variant = "destructive"
}) {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[400px] border border-slate-100 bg-white">
        <DialogHeader>
          <DialogTitle className="text-slate-800 font-bold">{title}</DialogTitle>
          <DialogDescription className="text-slate-400 text-xs mt-1.5 leading-relaxed">
            {description}
          </DialogDescription>
        </DialogHeader>
        <DialogFooter className="mt-4 gap-2">
          <Button
            variant="outline"
            onClick={onClose}
            className="text-xs font-semibold text-slate-500 border-slate-200 hover:bg-slate-50"
          >
            {cancelText}
          </Button>
          <Button
            variant={variant}
            onClick={() => {
              onConfirm()
              onClose()
            }}
            className={`text-xs font-semibold text-white ${
              variant === "destructive"
                ? "bg-rose-600 hover:bg-rose-700 shadow-md shadow-rose-100"
                : "bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-100"
            }`}
          >
            {confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
