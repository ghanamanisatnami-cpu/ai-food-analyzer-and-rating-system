CREATE DATABASE IF NOT EXISTS smart_product_analyzer
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_product_analyzer;

CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin','user') NOT NULL DEFAULT 'user',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  brand VARCHAR(150),
  category VARCHAR(80) NOT NULL,
  ingredients TEXT,
  barcode VARCHAR(80),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS compositions (
  composition_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  serving_size DECIMAL(10,2),
  serving_unit VARCHAR(20),
  is_current BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS nutrients (
  nutrient_id INT AUTO_INCREMENT PRIMARY KEY,
  composition_id INT NOT NULL,
  name VARCHAR(80) NOT NULL,
  value DECIMAL(12,4),
  unit VARCHAR(20) NOT NULL,
  basis VARCHAR(30) NOT NULL DEFAULT 'per_100g',
  FOREIGN KEY (composition_id) REFERENCES compositions(composition_id)
);

CREATE TABLE IF NOT EXISTS ingredients (
  ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
  composition_id INT NOT NULL,
  ingredient_name VARCHAR(200) NOT NULL,
  normalized_name VARCHAR(200),
  ingredient_category VARCHAR(100),
  risk_flag VARCHAR(80),
  FOREIGN KEY (composition_id) REFERENCES compositions(composition_id)
);

CREATE TABLE IF NOT EXISTS knowledge_rules (
  rule_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  field_name VARCHAR(80) NOT NULL,
  operator VARCHAR(10) NOT NULL,
  threshold DECIMAL(12,4) NOT NULL,
  weight DECIMAL(12,4) NOT NULL,
  unit VARCHAR(30) NOT NULL,
  rule_version VARCHAR(30) NOT NULL,
  source_ref VARCHAR(255) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analyses (
  analysis_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  composition_id INT NOT NULL,
  health_score DECIMAL(6,2) NOT NULL,
  health_category VARCHAR(40) NOT NULL,
  missing_fields TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (composition_id) REFERENCES compositions(composition_id)
);

CREATE TABLE IF NOT EXISTS analysis_factors (
  factor_id INT AUTO_INCREMENT PRIMARY KEY,
  analysis_id INT NOT NULL,
  rule_id INT NOT NULL,
  contribution DECIMAL(12,4) NOT NULL,
  evidence_value DECIMAL(12,4),
  FOREIGN KEY (analysis_id) REFERENCES analyses(analysis_id),
  FOREIGN KEY (rule_id) REFERENCES knowledge_rules(rule_id)
);

CREATE TABLE IF NOT EXISTS explanations (
  explanation_id INT AUTO_INCREMENT PRIMARY KEY,
  analysis_id INT NOT NULL,
  message TEXT NOT NULL,
  FOREIGN KEY (analysis_id) REFERENCES analyses(analysis_id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(120) NOT NULL,
  entity_type VARCHAR(80),
  entity_id INT,
  details TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
