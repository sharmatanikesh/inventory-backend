import base64
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Type
from uuid import UUID
from sqlalchemy import asc, desc, or_, and_

def encode_cursor(values: Dict[str, Any]) -> str:
    """Encodes cursor details (like sort value and tie-breaker id) as a base64 string."""
    serializable = {}
    for key, val in values.items():
        if isinstance(val, datetime):
            serializable[key] = val.isoformat()
        elif isinstance(val, UUID):
            serializable[key] = str(val)
        else:
            serializable[key] = val
    json_str = json.dumps(serializable)
    return base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

def decode_cursor(cursor_str: str) -> Dict[str, Any]:
    """Decodes a base64 encoded cursor string back to its dictionary values."""
    try:
        decoded_bytes = base64.b64decode(cursor_str.encode("utf-8"))
        return json.loads(decoded_bytes.decode("utf-8"))
    except Exception:
        raise ValueError("Invalid cursor format")

def paginate_list(
    items: List[Dict[str, Any]],
    cursor: Optional[str] = None,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "desc",
    id_key: str = "id"
) -> Tuple[List[Dict[str, Any]], Optional[str], bool]:
    """
    Paginates a python list of dicts using cursor-based pagination.
    Supports in-memory filtering, custom sorting, and tie-breaking.
    """
    if not items:
        return [], None, False

    for item in items:
        if sort_by not in item:
            raise ValueError(f"Sort key '{sort_by}' missing from item in list")
        if id_key not in item:
            raise ValueError(f"ID key '{id_key}' missing from item in list")

    def sort_key_func(item):
        val = item[sort_by]
        return (val, item[id_key])

    is_desc = order.lower() == "desc"
    items_sorted = sorted(items, key=sort_key_func, reverse=is_desc)

    filtered_items = items_sorted
    if cursor:
        cursor_data = decode_cursor(cursor)
        cursor_sort_val = cursor_data.get(sort_by)
        cursor_id_val = cursor_data.get(id_key)

        new_filtered = []
        for item in items_sorted:
            item_sort_val = item[sort_by]
            item_id_val = item[id_key]

            # Cast values to string if loaded as string from json
            if isinstance(cursor_sort_val, str) and not isinstance(item_sort_val, str):
                item_sort_val = str(item_sort_val)
            if isinstance(cursor_id_val, str) and not isinstance(item_id_val, str):
                item_id_val = str(item_id_val)

            if is_desc:
                if item_sort_val < cursor_sort_val:
                    new_filtered.append(item)
                elif item_sort_val == cursor_sort_val and item_id_val < cursor_id_val:
                    new_filtered.append(item)
            else:
                if item_sort_val > cursor_sort_val:
                    new_filtered.append(item)
                elif item_sort_val == cursor_sort_val and item_id_val > cursor_id_val:
                    new_filtered.append(item)
        
        filtered_items = new_filtered

    has_more = len(filtered_items) > limit
    paginated_items = filtered_items[:limit]

    next_cursor = None
    if has_more and paginated_items:
        last_item = paginated_items[-1]
        next_cursor_data = {
            sort_by: last_item[sort_by],
            id_key: last_item[id_key]
        }
        next_cursor = encode_cursor(next_cursor_data)

    return paginated_items, next_cursor, has_more

def paginate_query(
    query: Any,
    model_class: Type,
    cursor: Optional[str] = None,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "desc",
    id_column_name: str = "id"
) -> Tuple[List[Any], Optional[str], bool]:
    """
    Paginates a SQLAlchemy query using cursor-based pagination.
    Supports tie-breaker fields and custom sorts.
    """
    sort_col = getattr(model_class, sort_by, None)
    if sort_col is None:
        raise ValueError(f"Sort column '{sort_by}' does not exist on model {model_class.__name__}")
    
    id_col = getattr(model_class, id_column_name, None)
    if id_col is None:
        raise ValueError(f"ID column '{id_column_name}' does not exist on model {model_class.__name__}")

    if cursor:
        cursor_data = decode_cursor(cursor)
        cursor_sort_val = cursor_data.get(sort_by)
        cursor_id_val = cursor_data.get(id_column_name)
        
        if hasattr(sort_col.type, "python_type") and issubclass(sort_col.type.python_type, datetime):
            if cursor_sort_val:
                cursor_sort_val = datetime.fromisoformat(cursor_sort_val)
        
        if hasattr(id_col.type, "python_type") and issubclass(id_col.type.python_type, UUID):
            if cursor_id_val:
                cursor_id_val = UUID(cursor_id_val)

        if order.lower() == "desc":
            clause = or_(
                sort_col < cursor_sort_val,
                and_(sort_col == cursor_sort_val, id_col < cursor_id_val)
            )
        else:
            clause = or_(
                sort_col > cursor_sort_val,
                and_(sort_col == cursor_sort_val, id_col > cursor_id_val)
            )
        query = query.filter(clause)

    if order.lower() == "desc":
        query = query.order_by(desc(sort_col), desc(id_col))
    else:
        query = query.order_by(asc(sort_col), asc(id_col))

    items = query.limit(limit + 1).all()
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]
    
    next_cursor = None
    if has_more and items:
        last_item = items[-1]
        next_cursor_data = {
            sort_by: getattr(last_item, sort_by),
            id_column_name: getattr(last_item, id_column_name)
        }
        next_cursor = encode_cursor(next_cursor_data)

    return items, next_cursor, has_more
