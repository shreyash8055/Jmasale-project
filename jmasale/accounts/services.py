from .models import User

def create_user(data):
    return User.objects.create_user(**data)

def authenticate_user(username, password):
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        return user
    return None