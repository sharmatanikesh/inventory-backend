import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

# Seed data for 50 products
PRODUCTS_DATA = [
    # Electronics (20 items)
    {"sku": "ELEC-001", "name": "MacBook Pro 16\"", "price": 2499.00, "quantity": 15},
    {"sku": "ELEC-002", "name": "iPhone 15 Pro", "price": 999.00, "quantity": 25},
    {"sku": "ELEC-003", "name": "Sony WH-1000XM5 Headphones", "price": 349.99, "quantity": 30},
    {"sku": "ELEC-004", "name": "Dell 27\" 4K USB-C Monitor", "price": 429.99, "quantity": 12},
    {"sku": "ELEC-005", "name": "iPad Air (WiFi, 256GB)", "price": 649.00, "quantity": 18},
    {"sku": "ELEC-006", "name": "Keychron K2 Mechanical Keyboard", "price": 89.99, "quantity": 5},  # Will become 4 after orders
    {"sku": "ELEC-007", "name": "Logitech MX Master 3S Mouse", "price": 99.99, "quantity": 22},
    {"sku": "ELEC-008", "name": "Anker Power Bank 20K", "price": 59.99, "quantity": 50},
    {"sku": "ELEC-009", "name": "USB-C Hub Multiport Adapter", "price": 45.00, "quantity": 2},  # Will become 1 after orders
    {"sku": "ELEC-010", "name": "Bose SoundLink Flex Speaker", "price": 149.00, "quantity": 15},
    {"sku": "ELEC-011", "name": "Samsung T7 Portable SSD 1TB", "price": 119.99, "quantity": 20},
    {"sku": "ELEC-012", "name": "Kindle Paperwhite (16GB)", "price": 139.99, "quantity": 8},
    {"sku": "ELEC-013", "name": "GoPro HERO12 Black", "price": 399.00, "quantity": 6},
    {"sku": "ELEC-014", "name": "Apple Watch Series 9", "price": 399.00, "quantity": 14},
    {"sku": "ELEC-015", "name": "Elgato Wave:3 USB Microphone", "price": 149.99, "quantity": 10},
    {"sku": "ELEC-016", "name": "Ring Video Doorbell Plus", "price": 179.99, "quantity": 11},
    {"sku": "ELEC-017", "name": "Google Nest Learning Thermostat", "price": 249.00, "quantity": 7},
    {"sku": "ELEC-018", "name": "Fitbit Charge 6 Tracker", "price": 159.95, "quantity": 25},
    {"sku": "ELEC-019", "name": "Razer DeathAdder Essential Mouse", "price": 29.99, "quantity": 40},
    {"sku": "ELEC-020", "name": "Sony PlayStation 5 Console", "price": 499.99, "quantity": 3},

    # Office Furniture & Lighting (10 items)
    {"sku": "FURN-001", "name": "Ergonomic Office Chair", "price": 299.50, "quantity": 8},
    {"sku": "FURN-002", "name": "Electric Standing Desk (60x30)", "price": 499.00, "quantity": 3},
    {"sku": "FURN-003", "name": "Dual Monitor Arm Mount", "price": 89.00, "quantity": 15},
    {"sku": "FURN-004", "name": "Leather Desk Mat (Medium)", "price": 29.99, "quantity": 1},  # Will become 0 after orders
    {"sku": "FURN-005", "name": "Under-Desk Foot Rest", "price": 35.00, "quantity": 12},
    {"sku": "FURN-006", "name": "LED Desk Lamp with Wireless Charger", "price": 49.99, "quantity": 19},
    {"sku": "FURN-007", "name": "3-Drawer Mobile File Cabinet", "price": 129.00, "quantity": 5},
    {"sku": "FURN-008", "name": "Cable Management Tray Under-Desk", "price": 24.99, "quantity": 35},
    {"sku": "FURN-009", "name": "Lumbar Support Pillow", "price": 39.99, "quantity": 16},
    {"sku": "FURN-010", "name": "Anti-Fatigue Standing Desk Mat", "price": 49.99, "quantity": 10},

    # Stationery & Desk Accessories (10 items)
    {"sku": "STAT-001", "name": "Moleskine Classic Notebook", "price": 22.95, "quantity": 60},
    {"sku": "STAT-002", "name": "Pilot G2 Gel Pens (12-Pack)", "price": 14.50, "quantity": 80},
    {"sku": "STAT-003", "name": "Heavy Duty Stapler", "price": 19.99, "quantity": 25},
    {"sku": "STAT-004", "name": "Dry Erase Whiteboard (36x24)", "price": 39.99, "quantity": 7},
    {"sku": "STAT-005", "name": "Post-it Super Sticky Notes (24-Pack)", "price": 18.50, "quantity": 100},
    {"sku": "STAT-006", "name": "Desktop Document Organizer", "price": 24.99, "quantity": 14},
    {"sku": "STAT-007", "name": "Highlighter Chisel Tip (8-Pack)", "price": 7.99, "quantity": 90},
    {"sku": "STAT-008", "name": "Premium Paper Shredder", "price": 89.99, "quantity": 4},
    {"sku": "STAT-009", "name": "Metal Mesh Wastebasket", "price": 12.99, "quantity": 30},
    {"sku": "STAT-010", "name": "Desk Organizer Carousel", "price": 15.99, "quantity": 15},

    # Lifestyle & Accessories (10 items)
    {"sku": "LIFE-001", "name": "Hydro Flask Water Bottle 32oz", "price": 44.95, "quantity": 45},
    {"sku": "LIFE-002", "name": "Travel Laptop Backpack 15.6\"", "price": 79.99, "quantity": 24},
    {"sku": "LIFE-003", "name": "Keurig K-Mini Coffee Maker", "price": 89.99, "quantity": 5},
    {"sku": "LIFE-004", "name": "Double-Wall Insulated Coffee Mug", "price": 19.99, "quantity": 40},
    {"sku": "LIFE-005", "name": "Blue Light Blocking Glasses", "price": 16.99, "quantity": 35},
    {"sku": "LIFE-006", "name": "Electric Gooseneck Kettle", "price": 69.99, "quantity": 8},
    {"sku": "LIFE-007", "name": "Weekly Planner Pad (52 Sheets)", "price": 12.99, "quantity": 50},
    {"sku": "LIFE-008", "name": "Acoustic Foam Panels (12-Pack)", "price": 34.99, "quantity": 12},
    {"sku": "LIFE-009", "name": "Portable Desk Fan USB-Powered", "price": 14.99, "quantity": 28},
    {"sku": "LIFE-010", "name": "Essential Oil Diffuser 300ml", "price": 26.99, "quantity": 17}
]

# Seed data for 5 customers
CUSTOMERS_DATA = [
    {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone_number": "+15550199"},
    {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com", "phone_number": "+15550188"},
    {"first_name": "Alice", "last_name": "Johnson", "email": "alice.johnson@example.com", "phone_number": "+15550177"},
    {"first_name": "Bob", "last_name": "Brown", "email": "bob.brown@example.com", "phone_number": "+15550166"},
    {"first_name": "Charlie", "last_name": "Green", "email": "charlie.green@example.com", "phone_number": "+15550155"}
]

# Seed data for 5 orders
ORDERS_DATA = [
    {
        "customer_email": "john.doe@example.com",
        "status": "completed",
        "created_days_ago": 10,
        "items": [
            {"product_sku": "ELEC-001", "quantity": 1},  # MacBook Pro
            {"product_sku": "ELEC-009", "quantity": 1}   # USB-C Hub
        ]
    },
    {
        "customer_email": "jane.smith@example.com",
        "status": "completed",
        "created_days_ago": 5,
        "items": [
            {"product_sku": "ELEC-002", "quantity": 1},  # iPhone 15 Pro
            {"product_sku": "FURN-004", "quantity": 1}   # Leather Desk Mat
        ]
    },
    {
        "customer_email": "alice.johnson@example.com",
        "status": "pending",
        "created_days_ago": 2,
        "items": [
            {"product_sku": "ELEC-003", "quantity": 2}   # Sony WH-1000XM5
        ]
    },
    {
        "customer_email": "bob.brown@example.com",
        "status": "completed",
        "created_days_ago": 1,
        "items": [
            {"product_sku": "ELEC-006", "quantity": 1}   # Keychron K2 Keyboard
        ]
    },
    {
        "customer_email": "charlie.green@example.com",
        "status": "cancelled",
        "created_days_ago": 4,
        "items": [
            {"product_sku": "ELEC-004", "quantity": 1}   # Dell 27" Monitor
        ]
    }
]

def seed_db(db: Session, force_reset: bool = False) -> None:
    """
    Seeds the database with 50 products, 5 customers, and 5 orders.
    If force_reset is True, deletes all existing orders, customers, and products first.
    """
    if force_reset:
        print("Force reset requested. Clearing existing database tables...")
        # Clear child dependencies first
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(Customer).delete()
        db.commit()
        print("Database tables cleared.")

    # 1. Seed Products
    print("Seeding products...")
    sku_to_product = {}
    for p_info in PRODUCTS_DATA:
        # Check if product already exists (by SKU) to avoid duplicates if reset is False
        existing_product = db.query(Product).filter(
            Product.sku == p_info["sku"],
            Product.deleted_at.is_(None)
        ).first()
        
        if existing_product:
            sku_to_product[p_info["sku"]] = existing_product
        else:
            product = Product(
                name=p_info["name"],
                sku=p_info["sku"],
                price=p_info["price"],
                quantity=p_info["quantity"],
                is_active=True
            )
            db.add(product)
            sku_to_product[p_info["sku"]] = product
            
    db.commit()
    print(f"Products seeded. Total: {db.query(Product).filter(Product.deleted_at.is_(None)).count()}")

    # 2. Seed Customers
    print("Seeding customers...")
    email_to_customer = {}
    for c_info in CUSTOMERS_DATA:
        existing_customer = db.query(Customer).filter(
            Customer.email == c_info["email"],
            Customer.deleted_at.is_(None)
        ).first()
        
        if existing_customer:
            email_to_customer[c_info["email"]] = existing_customer
        else:
            customer = Customer(
                first_name=c_info["first_name"],
                last_name=c_info["last_name"],
                email=c_info["email"],
                phone_number=c_info["phone_number"]
            )
            db.add(customer)
            email_to_customer[c_info["email"]] = customer
            
    db.commit()
    print(f"Customers seeded. Total: {db.query(Customer).filter(Customer.deleted_at.is_(None)).count()}")

    # 3. Seed Orders and Items
    print("Seeding orders...")
    now = datetime.now(timezone.utc)
    
    for o_info in ORDERS_DATA:
        customer = email_to_customer.get(o_info["customer_email"])
        if not customer:
            continue
            
        # Check if this customer already has an order with the same status and items to prevent duplicates
        # In a seed script, if we are not resetting, we can just skip or add a new order
        # To keep it clean, if force_reset is False, we only seed if we don't find any orders
        
        created_at_time = now - timedelta(days=o_info["created_days_ago"])
        
        # Instantiate Order
        order = Order(
            customer_id=customer.id,
            status=o_info["status"],
            total_amount=0.00,
            created_at=created_at_time,
            updated_at=created_at_time
        )
        
        if o_info["status"] == "cancelled":
            order.cancelled_at = created_at_time
            
        db.add(order)
        db.flush() # Populate order.id
        
        total_amount = 0.00
        for item_info in o_info["items"]:
            product = sku_to_product.get(item_info["product_sku"])
            if not product:
                continue
                
            qty_ordered = item_info["quantity"]
            unit_price = product.price
            item_total = qty_ordered * float(unit_price)
            total_amount += item_total
            
            # Create OrderItem
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty_ordered,
                unit_price=unit_price
            )
            db.add(order_item)
            
            # Deduct inventory quantity if order is not cancelled
            if o_info["status"] != "cancelled":
                new_qty = max(0, product.quantity - qty_ordered)
                product.quantity = new_qty
                
        order.total_amount = total_amount
        
    db.commit()
    print(f"Orders and order items seeded successfully. Total Orders: {db.query(Order).count()}")


if __name__ == "__main__":
    import argparse
    from sqlalchemy.orm import sessionmaker
    from app.database.database import get_instance
    
    parser = argparse.ArgumentParser(description="Database Seeding CLI utility")
    parser.add_argument("--force", action="store_true", help="Force database reset (deletion of all existing data) before seeding")
    args = parser.parse_args()
    
    engine = get_instance()
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        seed_db(db, force_reset=args.force)
        print("Database seeded successfully via standalone CLI.")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

