-- Lost and Found Management System Database Schema
-- Normalized to Third Normal Form (3NF)

-- Drop existing tables if they exist
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS match_table CASCADE;
DROP TABLE IF EXISTS found_items CASCADE;
DROP TABLE IF EXISTS lost_items CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'admin')),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Lost Items Table
CREATE TABLE lost_items (
    lost_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    item_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location_lost VARCHAR(300) NOT NULL,
    date_lost DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'unfound' CHECK (status IN ('unfound', 'found', 'resolved')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Found Items Table
CREATE TABLE found_items (
    found_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    item_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location_found VARCHAR(300) NOT NULL,
    date_found DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'unclaimed' CHECK (status IN ('unclaimed', 'returned', 'resolved')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Match Table (many-to-many relationship between lost and found items)
CREATE TABLE match_table (
    match_id SERIAL PRIMARY KEY,
    lost_id INTEGER NOT NULL REFERENCES lost_items(lost_id) ON DELETE CASCADE,
    found_id INTEGER NOT NULL REFERENCES found_items(found_id) ON DELETE CASCADE,
    match_score DECIMAL(5,2) NOT NULL,
    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    UNIQUE(lost_id, found_id)
);

-- Notifications Table
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    match_id INTEGER REFERENCES match_table(match_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_lost_items_user ON lost_items(user_id);
CREATE INDEX idx_lost_items_status ON lost_items(status);
CREATE INDEX idx_lost_items_category ON lost_items(category);
CREATE INDEX idx_found_items_user ON found_items(user_id);
CREATE INDEX idx_found_items_status ON found_items(status);
CREATE INDEX idx_found_items_category ON found_items(category);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_match_table_lost ON match_table(lost_id);
CREATE INDEX idx_match_table_found ON match_table(found_id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_lost_items_updated_at
    BEFORE UPDATE ON lost_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_found_items_updated_at
    BEFORE UPDATE ON found_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default admin user (password: admin123)
INSERT INTO users (username, email, password_hash, full_name, role, phone)
VALUES ('admin', 'admin@lostandfound.com', 'scrypt:32768:8:1$9mElRpSVvycCtcEq$9052c5ab96e3f375670d721be2407f614a7737f45634bd60de444364b690687eb335e329447c90ff922162cf5426f9a12ab7aa30e0af9f91027f21bb2e62188a', 'System Administrator', 'admin', '0000000000');

-- Insert sample student users (password: student123)
INSERT INTO users (username, email, password_hash, full_name, role, phone)
VALUES 
('john_doe', 'john@student.edu', 'scrypt:32768:8:1$RInTwP3C7ONIBFgb$c435da40460f03ec9d907526f59ee7cb3f549fab6bbc010553cf8174ece1361d7aec25495871a2b9dd6d3755817a3549a7846b1da0935e768f4a2c134e3e5c98', 'John Doe', 'student', '1234567890'),
('jane_smith', 'jane@student.edu', 'scrypt:32768:8:1$RInTwP3C7ONIBFgb$c435da40460f03ec9d907526f59ee7cb3f549fab6bbc010553cf8174ece1361d7aec25495871a2b9dd6d3755817a3549a7846b1da0935e768f4a2c134e3e5c98', 'Jane Smith', 'student', '0987654321');

COMMENT ON TABLE users IS 'Stores user account information with role-based access';
COMMENT ON TABLE lost_items IS 'Records of items reported as lost by users';
COMMENT ON TABLE found_items IS 'Records of items reported as found by users';
COMMENT ON TABLE match_table IS 'Stores matches between lost and found items with similarity scores';
COMMENT ON TABLE notifications IS 'User notifications for potential item matches';
