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