-- ==========================================
-- BASELINE DATABASE SCHEMA
-- Inventory & Order Management System (PostgreSQL)
-- ==========================================

-- Enable PostgreSQL UUID generation capability (standard on PG 13+)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================
-- 0. TABLE: users
-- ==========================================
-- Stores user credentials, roles (ADMIN/CUSTOMER), and active status.
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'CUSTOMER' NOT NULL, -- ADMIN, CUSTOMER
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX idx_users_email_active ON users (email) WHERE deleted_at IS NULL;

-- ==========================================
-- 1. TABLE: customers
-- ==========================================
-- Stores customer profiles. Full name is split into first_name and last_name.
-- Email is unique among active (non-deleted) customers and indexed for fast retrieval.
-- Link to users credentials via user_id.
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT fk_customers_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Unique index on active customer emails only to allow reuse of email address after deletion
CREATE UNIQUE INDEX idx_customers_email_active ON customers (email) WHERE deleted_at IS NULL;

-- ==========================================
-- 1.5 TABLE: user_refresh_tokens
-- ==========================================
-- Stores user refresh token hashes to allow session revocation.
CREATE TABLE user_refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT fk_refresh_tokens_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_refresh_tokens_hash ON user_refresh_tokens (token_hash);


-- ==========================================
-- 2. TABLE: products
-- ==========================================
-- Stores product metadata, pricing, and current inventory levels.
-- SKU/code is unique among active products and indexed. Quantity is guarded to never fall below zero.
-- deleted_at stores the deletion timestamp for soft deletes and audit records.
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 0 NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    -- Prevent negative stock values under any race condition
    CONSTRAINT check_quantity_non_negative CHECK (quantity >= 0)
);

-- Unique index on active product SKUs only to allow reuse of SKU/code after deletion
CREATE UNIQUE INDEX idx_products_sku_active ON products (sku) WHERE deleted_at IS NULL;

-- ==========================================
-- 3. TABLE: orders
-- ==========================================
-- Header record for client orders. Contains status and pre-computed total amount.
-- Deleting a customer with active orders is RESTRICTED to preserve history.
-- cancelled_at stores when the order was cancelled, providing audit trail capabilities.
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    total_amount NUMERIC(12, 2) DEFAULT 0.00 NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL, -- pending, completed, cancelled
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    
    -- Restrict deletion of customers that have existing order records
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers (id) ON DELETE RESTRICT
);

-- Index on customer_id for fast customer order history retrieval
CREATE INDEX idx_orders_customer_id ON orders (customer_id);

-- Index on created_at for dashboard performance (recent orders, date filters)
CREATE INDEX idx_orders_created_at ON orders (created_at);

-- ==========================================
-- 4. TABLE: order_items
-- ==========================================
-- Line items for orders. Capture the quantity and unit_price at purchase time
-- to freeze historical transaction values. Deleting an order cascades to items.
-- Deleting a product referenced in an order is RESTRICTED (soft-delete product instead).
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Cascading order deletion (if order header is deleted, delete items)
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    
    -- Restrict product deletion to avoid dangling references in historic orders
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE RESTRICT,
    
    -- Enforce ordering at least 1 item
    CONSTRAINT check_quantity_positive CHECK (quantity > 0)
);

-- Indexes on foreign keys to optimize joins
CREATE INDEX idx_order_items_order_id ON order_items (order_id);
CREATE INDEX idx_order_items_product_id ON order_items (product_id);
