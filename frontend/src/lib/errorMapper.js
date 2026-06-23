export const COMMON_ERRORS = {
  DATABASE_CONNECTION_ERROR: "Database error: Unable to connect to the database service. Please try again later.",
  INSUFFICIENT_STOCK: "Order failed: Insufficient product stock available.",
  SKU_EXISTS: "Conflict: A product with this SKU code already exists.",
  EMAIL_EXISTS: "Conflict: A customer with this email address already exists.",
  RESOURCE_NOT_FOUND: "Resource not found: The requested item could not be retrieved.",
  NETWORK_ERROR: "Network error: Connection to the backend server failed. Please check your network connection.",
  INTERNAL_SERVER_ERROR: "Server error: The server encountered an unexpected error. Please try again later.",
  VALIDATION_ERROR: "Validation error: Please verify that all fields are correct.",
  DEFAULT_FAILED: "Request failed: The server could not process the request."
}

/**
 * Maps any raw technical API or network error into a clean, user-friendly message.
 * @param {any} rawError The raw error from the API/thunk rejection
 * @returns {string} User-friendly error message
 */
export function getErrorMessage(rawError) {
  if (!rawError) return COMMON_ERRORS.DEFAULT_FAILED
  
  const errorStr = String(rawError).toLowerCase()
  
  // 502 Bad Gateway / Server Down
  if (errorStr.includes("502") || errorStr.includes("bad gateway")) {
    return COMMON_ERRORS.NETWORK_ERROR
  }

  // Database / Connection / Operational errors
  if (
    errorStr.includes("operationalerror") || 
    errorStr.includes("connection to server") || 
    errorStr.includes("database") || 
    errorStr.includes("pg_isready") ||
    errorStr.includes("conn") ||
    errorStr.includes("refused")
  ) {
    return COMMON_ERRORS.DATABASE_CONNECTION_ERROR
  }

  
  // Business logic exceptions
  if (errorStr.includes("insufficient stock") || errorStr.includes("insufficientstock")) {
    return COMMON_ERRORS.INSUFFICIENT_STOCK
  }
  if (errorStr.includes("sku") && errorStr.includes("exists")) {
    return COMMON_ERRORS.SKU_EXISTS
  }
  if (errorStr.includes("email") && errorStr.includes("exists")) {
    return COMMON_ERRORS.EMAIL_EXISTS
  }
  if (errorStr.includes("not found") || errorStr.includes("notfound") || errorStr.includes("404")) {
    return COMMON_ERRORS.RESOURCE_NOT_FOUND
  }
  if (errorStr.includes("network") || errorStr.includes("err_connection") || errorStr.includes("network error")) {
    return COMMON_ERRORS.NETWORK_ERROR
  }
  if (errorStr.includes("500") || errorStr.includes("internal server error")) {
    return COMMON_ERRORS.INTERNAL_SERVER_ERROR
  }
  if (errorStr.includes("validation") || errorStr.includes("unprocessable")) {
    return COMMON_ERRORS.VALIDATION_ERROR
  }
  
  // If the error message is already clean/short and doesn't contain technical traceback terms,
  // return it directly.
  if (
    rawError.length < 60 && 
    !errorStr.includes("exception") && 
    !errorStr.includes("error") && 
    !errorStr.includes("failed") &&
    !errorStr.includes("500")
  ) {
    return rawError
  }
  
  return COMMON_ERRORS.DEFAULT_FAILED
}
