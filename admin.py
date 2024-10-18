from db import session, User

# List all users
def list_users():
    users = session.query(User).all()
    return users

# Other admin-related functions...
