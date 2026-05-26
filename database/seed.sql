PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
  customer_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  unit_price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT OR IGNORE INTO customers (customer_id, name, email, created_at) VALUES
  (1, 'Acme Corp', 'buyer@acme.example', '2026-01-05'),
  (2, 'Globex', 'sales@globex.example', '2026-02-12'),
  (3, 'Initech', 'ap@initech.example', '2026-03-20');

INSERT OR IGNORE INTO products (product_id, name, category, unit_price) VALUES
  (1, 'Widget', 'Hardware', 19.99),
  (2, 'Gadget', 'Hardware', 29.50),
  (3, 'Analytics Subscription', 'Software', 99.00),
  (4, 'Support Plan', 'Services', 49.00);

INSERT OR IGNORE INTO orders (order_id, customer_id, order_date, status) VALUES
  (1001, 1, '2026-04-02', 'paid'),
  (1002, 1, '2026-05-10', 'paid'),
  (1003, 2, '2026-05-15', 'paid'),
  (1004, 3, '2026-05-22', 'pending');

INSERT OR IGNORE INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
  (5001, 1001, 1, 10, 19.99),
  (5002, 1001, 4, 1, 49.00),
  (5003, 1002, 2, 5, 29.50),
  (5004, 1002, 3, 1, 99.00),
  (5005, 1003, 3, 2, 99.00),
  (5006, 1004, 1, 3, 19.99);

