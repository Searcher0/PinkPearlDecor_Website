CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE ClientDetails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    initial_contact VARCHAR(100),
    point_of_contact VARCHAR(100),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE EmployeeDetails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100),
    role VARCHAR(20),
    permissions VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Meetings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    employee_id INT,
    scheduled_at DATETIME,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES ClientDetails(id),
    FOREIGN KEY (employee_id) REFERENCES EmployeeDetails(id)
);

CREATE TABLE Presets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    contract_details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES ClientDetails(id)
);

CREATE TABLE Feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    feedback TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES ClientDetails(id)
);

CREATE TABLE Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50)
);

CREATE TABLE Permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(50)
);

CREATE TABLE RolePermissions (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Roles(id),
    FOREIGN KEY (permission_id) REFERENCES Permissions(id)
);
