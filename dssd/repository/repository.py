from django.contrib.auth.models import User

class Repository(object):
    def find_user_by_email(self, email):
        users_filtered = User.objects.filter(username = email)
        return users_filtered[0] if len(users_filtered) > 0 else None

    def add_user(self, email, password):
        if not self.find_user_by_email(email):
            user = User.objects.create_user(username = email, password = password)
            return True
        return False