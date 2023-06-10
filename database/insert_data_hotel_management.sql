USE hotel_management;

-- Insert dummy data into the Roles table
INSERT INTO Roles (role_id, role_name) VALUES
  (1, 'admin'),
  (2, 'customer');

-- Insert dummy data into the User table
INSERT INTO Users (user_id, user_name, user_email, user_password, role_id) VALUES
  (1, 'Alex', 'alex@example.com', '$2b$12$wGnxMvrC/Lq05KrEDK5jvOyYAAJGRkjd.e.7JBxsQePoHr0rs4c7q', 2),
  (2, 'Mia', 'mia@example.com', '$2b$12$X0oyM.0xffNFx.9mkIQ1fekUV7SpAtBRz4rgzIUSL2XJHG3s8YNSe', 2),
  (3, 'Admin', 'admin@example.com', '$2b$12$kGjEGQ6VksuoCVibw4jhIObp8sfaCXU0k5bk/GGSGOda9Emu46Fhy', 1);
  
-- Insert dummy data into the RoomTypes table
INSERT INTO RoomTypes (type_id, type_name, price, info) VALUES
  (1, 'Standard Room', 100.00, 'Enjoy a relaxing stay in a well-appointed room with a warm ambiance.'),
  (2, 'Deluxe Room', 150.00, 'Indulge in luxury and sophistication with Our Deluxe Rooms. '),
  (3, 'Suite', 250.00, 'Experience the pinnacle of luxury in our exquisite Suites.');

-- Insert dummy data into the Service table
INSERT INTO Service (service_id, service_name, price, status) VALUES
  (1, 'Breakfast', 10.00, 1),
  (2, 'Extra Bed', 20.00, 1);

-- Insert dummy data into the RoomInventory table
INSERT INTO RoomInventory (inventory_id, room_type_id, available_rooms) VALUES
  (1, 1, 10),
  (2, 2, 5),
  (3, 3, 2);

-- Insert dummy data into the Bookings table
INSERT INTO Bookings (booking_id, user_id, user_full_name, user_phone, room_type_id, check_in_date, check_out_date, breakfast_amount, extra_bed_amount, status) VALUES
  (1, 1, 'John Doe', '12333333', 2, '2023-06-10', '2023-06-12', 1, 0, "Pending"),
  (2, 2, 'Jane Alex', '21112333', 1, '2023-06-15', '2023-06-20', 0, 1, "Pending");
