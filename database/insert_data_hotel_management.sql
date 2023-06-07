USE hotel_management;

-- Insert dummy data into the Roles table
INSERT INTO Roles (role_id, role_name) VALUES
  (1, 'admin'),
  (2, 'customer');

-- Insert dummy data into the User table
INSERT INTO Users (user_id, user_name, user_email, user_password, role_id) VALUES
  (1, 'John', 'johndoe@example.com', 'password123', 2),
  (2, 'Jane', 'janesmith@example.com', 'password456', 2),
  (3, 'Admin', 'admin@example.com', '$2b$12$kGjEGQ6VksuoCVibw4jhIObp8sfaCXU0k5bk/GGSGOda9Emu46Fhy', 1),
  (4, 'Mia', 'mia@example.com', '$2b$12$/n86suJI9IGaC7wj2nK4tu7xLLZUYgkbG3ufrrfWB5jjW9PbuTzc', 2);
  
-- Insert dummy data into the RoomTypes table
INSERT INTO RoomTypes (type_id, type_name, price, info) VALUES
  (1, 'Standard Room', 100.00, 'Our Standard Rooms offer a comfortable and cozy stay with all the essential amenities. These rooms are perfect for budget-conscious travelers without compromising on quality and comfort.'),
  (2, 'Deluxe Room', 150.00, 'Indulge in luxury and sophistication with our Deluxe Rooms. These spacious and elegantly designed rooms provide a blend of comfort and style. '),
  (3, 'Suite', 250.00, 'Experience the pinnacle of luxury in our exquisite Suites. These expansive and lavishly furnished accommodations offer a separate living area and bedroom, providing ample space for relaxation and entertainment.');

-- Insert dummy data into the Room table
INSERT INTO Room (room_id, type_id, status) VALUES
  (1, 1, 'Available'),
  (2, 2, 'Booked');

-- Insert dummy data into the Service table
INSERT INTO Service (service_id, service_name, price) VALUES
  (1, 'Breakfast', 10.00),
  (2, 'Extra Bed', 20.00);

-- Insert dummy data into the RoomInventory table
INSERT INTO RoomInventory (inventory_id, room_type_id, available_rooms) VALUES
  (1, 1, 10),
  (2, 2, 5),
  (3, 3, 2);

-- Insert dummy data into the Bookings table
INSERT INTO Bookings (booking_id, user_id, room_id, check_in_date, check_out_date, service_id, service_amount) VALUES
  (1, 1, 2, '2023-06-10', '2023-06-12', 1, 10.00),
  (2, 2, 1, '2023-06-15', '2023-06-20', 2, 20.00);
