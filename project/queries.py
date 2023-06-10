 # login employee role query  
def login():
    query= ("""
             SELECT * FROM Users WHERE user_email = %s
        """)
    return query

def register():
    query=('insert into Users (user_name, user_password, user_email, role_id) values (%s, %s, %s, %s)')
    return query

def googleRegister():
    query=('insert into Users (user_name, role_id) values (%s, %s)')
    return query

def googleUser():
    query=('select * from Users where role_id = 2 and user_name = %s order by user_id desc')
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

def searchRoom():
    query=('select * from RoomTypes where type_name=%s')
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
    query=('select * from Bookings join RoomTypes on Bookings.room_type_id = RoomTypes.type_id where user_id=%s order by booking_id desc;')
    return query

def bookingBill():
    query=('select * from Bookings where user_id=%s order by booking_id desc;')
    return query

def billInfo():
    query=('''
          select booking_id, user_id, user_full_name, user_phone, room_type_id, datediff(check_out_date, check_in_date) as duration, breakfast_amount, extra_bed_amount, status, RoomTypes.type_name, RoomTypes.price
          from Bookings
          join RoomTypes on Bookings.room_type_id = RoomTypes.type_id where booking_id=%s;
    ''')
    return query

def billConfirm():
    query=('update Bookings set status = "Confirmed" where booking_id=%s;')
    return query


def billCancel():
    query=('update Bookings set status = "Cancelled" where booking_id=%s;')
    return query