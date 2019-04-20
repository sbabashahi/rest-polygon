from django.contrib.auth.models import User
from django.db import transaction


@transaction.atomic
def register_user_with_email_and_password(email, password):
    user = User(email=email, username=email)
    user.set_password(password)
    user.save()
    return user
