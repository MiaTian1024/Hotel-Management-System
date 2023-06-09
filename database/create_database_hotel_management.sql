drop database hotel_management;
create database if not exists hotel_management;

USE hotel_management;

CREATE TABLE Roles (
  role_id INT PRIMARY KEY AUTO_INCREMENT,
  role_name VARCHAR(50)
);

CREATE TABLE Users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  user_name VARCHAR(50),
  user_email VARCHAR(100),
  user_password VARCHAR(100),
  role_id INT,
  FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

CREATE TABLE RoomTypes (
  type_id INT PRIMARY KEY AUTO_INCREMENT,
  type_name VARCHAR(50),
  price DECIMAL(10, 2),
  info VARCHAR(255)
);

CREATE TABLE Service (
  service_id INT PRIMARY KEY AUTO_INCREMENT,
  service_name VARCHAR(50),
  price DECIMAL(10, 2),
  status tinyint DEFAULT NULL
);

CREATE TABLE RoomInventory (
  inventory_id INT PRIMARY KEY AUTO_INCREMENT,
  room_type_id INT,
  available_rooms INT,
  FOREIGN KEY (room_type_id) REFERENCES RoomTypes(type_id)
);

CREATE TABLE Bookings (
  booking_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  user_full_name VARCHAR(50),
  user_phone VARCHAR(20),
  room_type_id INT,
  check_in_date DATE,
  check_out_date DATE,
  breakfast_amount INT DEFAULT NULL,
  extra_bed_amount INT DEFAULT NULL,
  status VARCHAR(50),
  FOREIGN KEY (user_id) REFERENCES Users(user_id),
  FOREIGN KEY (room_type_id) REFERENCES RoomTypes(type_id)
);
