 # login employee role query  
def login():
    query= ("""
             SELECT * FROM Users WHERE user_email = %s
        """)
    return query

def register():
    query=('insert into Users (user_name, user_password, user_email, role_id) values (%s, %s, %s, %s)')
    return query

def adminInfo():
    query=('select * from Users where role_id = 1 and user_id = %s')
    return query

def customerInfo():
    query=('select * from Users where role_id = 2 and user_id = %s')
    return query

def roomInfo():
    query=('select * from RoomTypes')
    return query

def service():
    query=('select * from Service')
    return query

def roomTypes():
    query=('select * from RoomTypes join RoomInventory on RoomInventory.room_type_id = RoomTypes.type_id;')
    return query

def typeInfo():
    query=('select * from RoomTypes where type_id=%s;')
    return query

def addBooking():
    query=("""
         insert into Bookings (user_id, user_full_name, user_phone, room_type_id, check_in_date, check_out_date, breakfast_amount, extra_bed_amount, status)
         values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
    return query

def bookingInfo():
    query=('select * from Bookings where user_id=%s;')
    return query