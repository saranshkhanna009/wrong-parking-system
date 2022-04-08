# Django Imports
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, first_name, mobile_number=None, email=None, password=None, **kwargs):
        """
        Creates And Saves A User.
        """
        if not first_name:
            raise ValueError('Users must have a First Name')

        user = self.model(
            first_name=first_name,
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, mobile_number=None, email=None, password=None, **kwargs):
        """
        Creates And Saves A Superuser.
        """
        user = self.create_user(
            first_name=first_name,
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user