from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, role=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
            )
        user.set_password(password)
        if role == 'administrator':
            user.is_superuser = True
            user.is_active = True
            user.is_admin = True
            user.is_staff = True
        if role: user.role = role
        user.save(using=self._db)
        return user

    
    def create_partner(self, email, password=None, **extra_fields):
        return self.create_user(
            email, 
            role='partner', 
            password=password, 
            **extra_fields
            )
    
    
    def create_regular_user(self, email, password=None, **extra_fields):
        return self.create_user(
            email, 
            role='regularuser', 
            password=password, 
            **extra_fields
            )

    
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
