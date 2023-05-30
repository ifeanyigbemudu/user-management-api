def user_serializer(user) -> dict:
    if user is not None:
        return {
            "_id": str(user["_id"]),
            "email": user.get("email"),
            "password": user.get("password"),
            "logged_in": user.get("logged_in")
        }
    else:
        return {}
    

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]