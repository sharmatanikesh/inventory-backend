import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.pagination import paginate_list

class PaginationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        query_params = request.query_params
        paginate_param = query_params.get("paginate", "").lower()
        
        # We only intercept GET requests requesting pagination
        if request.method != "GET" or paginate_param != "true":
            return await call_next(request)

        cursor = query_params.get("cursor")
        limit_str = query_params.get("limit", "10")
        sort_by = query_params.get("sort_by", "id")
        order = query_params.get("order", "desc")
        
        try:
            limit = int(limit_str)
        except ValueError:
            limit = 10

        response = await call_next(request)

        # Only process successful JSON responses
        content_type = response.headers.get("content-type", "")
        if response.status_code == 200 and "application/json" in content_type:
            # Consume the response body robustly
            if hasattr(response, "body_iterator"):
                body_parts = [section async for section in response.body_iterator]
                body = b"".join(body_parts)
            else:
                body = response.body
            
            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                # Reconstruct response if parsing fails
                return Response(content=body, status_code=response.status_code, headers=dict(response.headers))

            is_wrapped = isinstance(data, dict) and data.get("success") is True and isinstance(data.get("data"), list)
            
            if isinstance(data, list) or is_wrapped:
                list_to_paginate = data.get("data") if is_wrapped else data
                try:
                    paginated_items, next_cursor, has_more = paginate_list(
                        items=list_to_paginate,
                        cursor=cursor,
                        limit=limit,
                        sort_by=sort_by,
                        order=order
                    )
                    
                    pagination_info = {
                        "next_cursor": next_cursor,
                        "limit": limit,
                        "has_more": has_more
                    }
                    
                    if is_wrapped:
                        data["data"] = {
                            "items": paginated_items,
                            "pagination": pagination_info
                        }
                        paginated_response = data
                    else:
                        paginated_response = {
                            "items": paginated_items,
                            "pagination": pagination_info
                        }
                    
                    new_body = json.dumps(paginated_response).encode("utf-8")
                    
                    new_headers = dict(response.headers)
                    new_headers["content-length"] = str(len(new_body))
                    
                    return Response(
                        content=new_body,
                        status_code=response.status_code,
                        headers=new_headers,
                        media_type="application/json"
                    )
                except Exception as e:
                    error_body = json.dumps({
                        "detail": f"Pagination error: {str(e)}",
                        "error_code": "PAGINATION_ERROR"
                    }).encode("utf-8")
                    
                    new_headers = dict(response.headers)
                    new_headers["content-length"] = str(len(error_body))
                    return Response(
                        content=error_body,
                        status_code=400,
                        headers=new_headers,
                        media_type="application/json"
                    )
            else:
                # Reconstruct original response if body is not a JSON list
                return Response(content=body, status_code=response.status_code, headers=dict(response.headers))

        return response
