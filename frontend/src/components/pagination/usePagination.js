import { useState, useMemo, useEffect } from "react"

export default function usePagination(items = [], itemsPerPage = 20) {
  const [currentPage, setCurrentPage] = useState(1)

  const totalItems = items.length
  const totalPages = Math.max(1, Math.ceil(totalItems / itemsPerPage))

  // Handle case where items shrink and current page exceeds total pages
  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages)
    }
  }, [totalItems, totalPages, currentPage])

  const paginatedItems = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    return items.slice(startIndex, endIndex)
  }, [items, currentPage, itemsPerPage])

  return {
    currentPage,
    setCurrentPage,
    paginatedItems,
    totalPages,
    totalItems,
  }
}
