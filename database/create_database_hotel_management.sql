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
  price DECIMAL(10, 2)
);

CREATE TABLE Room (
  room_id INT PRIMARY KEY AUTO_INCREMENT,
  type_id INT,
  status VARCHAR(50),
  FOREIGN KEY (type_id) REFERENCES RoomTypes(type_id)
);

CREATE TABLE Service (
  service_id INT PRIMARY KEY AUTO_INCREMENT,
  service_name VARCHAR(50),
  price DECIMAL(10, 2)
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
  room_id INT,
  check_in_date DATE,
  check_out_date DATE,
  service_id INT,
  service_amount DECIMAL(10, 2),
  FOREIGN KEY (user_id) REFERENCES Users(user_id),
  FOREIGN KEY (room_id) REFERENCES Room(room_id),
  FOREIGN KEY (service_id) REFERENCES Service(service_id)
);
