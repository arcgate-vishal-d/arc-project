from django.contrib.auth.models import User


def format_user_json_data(user_obj: User):
    return {
        "id": user_obj.id,
        "username": user_obj.username,
        "email": user_obj.email,
        "is_active": user_obj.is_active,
        "is_superuser": user_obj.is_superuser,
        "is_staff": user_obj.is_staff,
    }
