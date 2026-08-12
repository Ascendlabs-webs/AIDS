import sqlite3

# =====================================================
# CONNECT TO DATABASE
# =====================================================

connection = sqlite3.connect("grocery_store.db")
cursor = connection.cursor()


# =====================================================
# 1. CUSTOMERS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    phone TEXT
)
""")


# =====================================================
# 2. SUPPLIERS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    contact TEXT
)
""")


# =====================================================
# 3. PRODUCTS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    supplier_id INTEGER,

    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
)
""")


# =====================================================
# 4. INVENTORY TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    stock_quantity INTEGER,
    reorder_level INTEGER,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
)
""")


# =====================================================
# 5. ORDERS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")


# =====================================================
# 6. ORDER ITEMS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
)
""")


# =====================================================
# INSERT CUSTOMERS
# =====================================================

customers = [
    (1, "Arun Kumar", "Chennai", "9876543210"),
    (2, "Priya Sharma", "Bangalore", "9876543211"),
    (3, "Rahul Menon", "Chennai", "9876543212"),
    (4, "Anitha Raj", "Hyderabad", "9876543213"),
    (5, "Karthik S", "Mumbai", "9876543214"),
    (6, "Divya Krishnan", "Chennai", "9876543215"),
    (7, "Vijay Kumar", "Coimbatore", "9876543216"),
    (8, "Sneha R", "Bangalore", "9876543217")
]

cursor.executemany("""
INSERT OR IGNORE INTO customers
VALUES (?, ?, ?, ?)
""", customers)


# =====================================================
# INSERT SUPPLIERS
# =====================================================

suppliers = [
    (1, "Sri Lakshmi Foods", "Chennai", "9000000001"),
    (2, "Fresh Farm Suppliers", "Coimbatore", "9000000002"),
    (3, "Green Basket Distributors", "Bangalore", "9000000003"),
    (4, "Daily Dairy Supplies", "Chennai", "9000000004"),
    (5, "South India Grocers", "Madurai", "9000000005")
]

cursor.executemany("""
INSERT OR IGNORE INTO suppliers
VALUES (?, ?, ?, ?)
""", suppliers)


# =====================================================
# INSERT PRODUCTS
# =====================================================

products = [
    (1, "India Gate Basmati Rice 5kg", "Grains", 450, 1),
    (2, "Aashirvaad Atta 5kg", "Grains", 280, 1),
    (3, "Toor Dal 1kg", "Pulses", 160, 1),
    (4, "Fortune Sunflower Oil 1L", "Oil", 140, 1),
    (5, "Aavin Milk 1L", "Dairy", 60, 4),
    (6, "Aavin Curd 500g", "Dairy", 40, 4),
    (7, "Farm Eggs 12 Pack", "Dairy", 90, 4),
    (8, "Tomato 1kg", "Vegetables", 50, 2),
    (9, "Potato 1kg", "Vegetables", 40, 2),
    (10, "Onion 1kg", "Vegetables", 45, 2),
    (11, "Carrot 1kg", "Vegetables", 70, 2),
    (12, "Apple 1kg", "Fruits", 160, 3),
    (13, "Banana 1 Dozen", "Fruits", 70, 3),
    (14, "Orange 1kg", "Fruits", 120, 3),
    (15, "Mango 1kg", "Fruits", 150, 3),
    (16, "Maggi Noodles 4 Pack", "Snacks", 60, 5),
    (17, "Parle-G Biscuits", "Snacks", 30, 5),
    (18, "Lays Potato Chips", "Snacks", 40, 5),
    (19, "Surf Excel 1kg", "Household", 180, 5),
    (20, "Vim Dishwash Bar", "Household", 30, 5)
]

cursor.executemany("""
INSERT OR IGNORE INTO products
VALUES (?, ?, ?, ?, ?)
""", products)


# =====================================================
# INSERT INVENTORY
# =====================================================

inventory = [
    (1, 1, 25, 10),
    (2, 2, 40, 15),
    (3, 3, 35, 10),
    (4, 4, 30, 10),
    (5, 5, 80, 25),
    (6, 6, 60, 20),
    (7, 7, 45, 15),
    (8, 8, 12, 20),
    (9, 9, 50, 20),
    (10, 10, 18, 25),
    (11, 11, 35, 15),
    (12, 12, 40, 15),
    (13, 13, 65, 20),
    (14, 14, 30, 10),
    (15, 15, 25, 10),
    (16, 16, 55, 20),
    (17, 17, 70, 25),
    (18, 18, 45, 15),
    (19, 19, 20, 10),
    (20, 20, 50, 15)
]

cursor.executemany("""
INSERT OR IGNORE INTO inventory
VALUES (?, ?, ?, ?)
""", inventory)


# =====================================================
# INSERT ORDERS
# =====================================================

orders = [
    (1, 1, "2026-01-05"),
    (2, 2, "2026-01-10"),
    (3, 3, "2026-01-18"),
    (4, 4, "2026-02-02"),
    (5, 5, "2026-02-15"),
    (6, 1, "2026-02-25"),
    (7, 6, "2026-03-05"),
    (8, 7, "2026-03-12"),
    (9, 8, "2026-03-20"),
    (10, 2, "2026-04-01"),
    (11, 3, "2026-04-15"),
    (12, 4, "2026-04-25"),
    (13, 5, "2026-05-05"),
    (14, 6, "2026-05-18"),
    (15, 7, "2026-06-01"),
    (16, 8, "2026-06-10"),
    (17, 1, "2026-06-20"),
    (18, 2, "2026-07-01"),
    (19, 3, "2026-07-15"),
    (20, 4, "2026-07-25")
]

cursor.executemany("""
INSERT OR IGNORE INTO orders
VALUES (?, ?, ?)
""", orders)


# =====================================================
# INSERT ORDER ITEMS
# =====================================================

order_items = [
    (1, 1, 1, 2, 450),
    (2, 1, 5, 3, 60),

    (3, 2, 2, 2, 280),
    (4, 2, 8, 3, 50),

    (5, 3, 12, 2, 160),
    (6, 3, 13, 3, 70),

    (7, 4, 5, 5, 60),
    (8, 4, 6, 2, 40),

    (9, 5, 1, 1, 450),
    (10, 5, 3, 2, 160),

    (11, 6, 9, 4, 40),
    (12, 6, 10, 3, 45),

    (13, 7, 7, 2, 90),
    (14, 7, 14, 2, 120),

    (15, 8, 4, 3, 140),
    (16, 8, 16, 2, 60),

    (17, 9, 11, 2, 70),
    (18, 9, 18, 3, 40),

    (19, 10, 1, 1, 450),
    (20, 10, 2, 2, 280),

    (21, 11, 5, 4, 60),
    (22, 11, 13, 5, 70),

    (23, 12, 19, 2, 180),
    (24, 12, 20, 3, 30),

    (25, 13, 3, 3, 160),
    (26, 13, 8, 5, 50),

    (27, 14, 12, 2, 160),
    (28, 14, 15, 2, 150),

    (29, 15, 6, 4, 40),
    (30, 15, 7, 2, 90),

    (31, 16, 16, 4, 60),
    (32, 16, 17, 5, 30),

    (33, 17, 1, 2, 450),
    (34, 17, 4, 2, 140),

    (35, 18, 9, 5, 40),
    (36, 18, 10, 4, 45),

    (37, 19, 5, 6, 60),
    (38, 19, 6, 3, 40),

    (39, 20, 12, 3, 160),
    (40, 20, 18, 4, 40)
]

cursor.executemany("""
INSERT OR IGNORE INTO order_items
VALUES (?, ?, ?, ?, ?)
""", order_items)


# =====================================================
# SAVE DATABASE
# =====================================================

connection.commit()
connection.close()

print("======================================")
print("GROCERY STORE DATABASE CREATED!")
print("======================================")
print("Customers     : 8")
print("Suppliers     : 5")
print("Products      : 20")
print("Inventory     : 20")
print("Orders        : 20")
print("Order Items   : 40")
print("======================================")