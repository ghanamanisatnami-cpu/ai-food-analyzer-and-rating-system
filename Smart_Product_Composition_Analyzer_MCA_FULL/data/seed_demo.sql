USE smart_product_analyzer;

INSERT INTO users(username,password_hash,role) VALUES
('admin','$2y$12$itEzL4wn.ipSxOrUg0V53.7QDEJuZMmizHhZe6vL3xqyfcRo5K3TK','admin'),
('demo','$2y$12$qyqi4/4YWGFuJYgfw/qBxeQighKXijxJZU8y2zn1E938JLPKppNf6','user');

INSERT INTO products(user_id,name,brand,category,ingredients,barcode) VALUES
(2,'Demo Oat Crunch','Sample Foods','Cereal',
 'Whole grain oats, sugar, sunflower oil, salt, fibre','890000000001'),
(2,'Demo Chocolate Snack','Sample Foods','Snack',
 'Wheat flour, sugar, glucose syrup, cocoa powder, salt','890000000002');

-- Demo credentials: admin/admin123 and demo/demo123. Change these credentials before deployment.
