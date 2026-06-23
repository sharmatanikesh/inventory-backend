import React from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "../ui/button"

export default function Pagination({
  currentPage,
  totalItems,
  itemsPerPage = 20,
  onPageChange
}) {
  const totalPages = Math.max(1, Math.ceil(totalItems / itemsPerPage))
  
  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1)
    }
  }

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1)
    }
  }

  const handlePageClick = (pageNumber) => {
    onPageChange(pageNumber)
  }

  // Calculate entry indices for info text
  const startEntry = totalItems === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1
  const endEntry = Math.min(currentPage * itemsPerPage, totalItems)

  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages = []
    const maxVisiblePages = 5

    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      // Always show page 1
      pages.push(1)

      let start = Math.max(2, currentPage - 1)
      let end = Math.min(totalPages - 1, currentPage + 1)

      if (currentPage <= 2) {
        end = 4
      } else if (currentPage >= totalPages - 1) {
        start = totalPages - 3
      }

      if (start > 2) {
        pages.push("ellipsis-start")
      }

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      if (end < totalPages - 1) {
        pages.push("ellipsis-end")
      }

      // Always show last page
      pages.push(totalPages)
    }
    return pages
  }

  const pageNumbers = getPageNumbers()

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-slate-100/80 pt-5 mt-4">
      {/* Entries summary */}
      <div className="text-xs text-slate-400 font-medium">
        Showing <span className="font-semibold text-slate-700">{startEntry}</span> to{" "}
        <span className="font-semibold text-slate-700">{endEntry}</span> of{" "}
        <span className="font-semibold text-slate-700">{totalItems}</span> entries
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center gap-1.5">
        <Button
          variant="outline"
          size="icon"
          onClick={handlePrevious}
          disabled={currentPage === 1}
          className="h-8 w-8 rounded-lg border-slate-200 text-slate-500 hover:bg-slate-50 disabled:opacity-40 transition-colors"
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>

        {pageNumbers.map((page, index) => {
          if (page === "ellipsis-start" || page === "ellipsis-end") {
            return (
              <span key={`ellipsis-${index}`} className="px-2 text-slate-400 text-xs font-bold">
                ...
              </span>
            )
          }

          const isActive = page === currentPage

          return (
            <button
              key={page}
              onClick={() => handlePageClick(page)}
              className={`h-8 min-w-[32px] px-2 rounded-lg text-xs font-bold transition-all duration-200 ${
                isActive
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-100"
                  : "border border-transparent text-slate-600 hover:bg-slate-100 hover:text-slate-800"
              }`}
            >
              {page}
            </button>
          )
        })}

        <Button
          variant="outline"
          size="icon"
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className="h-8 w-8 rounded-lg border-slate-200 text-slate-500 hover:bg-slate-50 disabled:opacity-40 transition-colors"
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
