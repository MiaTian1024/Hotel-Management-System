 # login employee role query  
def login():
    query= ("""
             SELECT * FROM Users WHERE user_email = %s
        """)
    return query

def register():
    query=('insert into Users (user_name, user_password, user_email, role_id) values (%s, %s, %s, %s)')
    return query