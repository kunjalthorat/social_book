#accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=255, default='Default Name')
    gender = models.CharField(max_length=100, default='Not Specified')
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    public_visibility = models.BooleanField(default=False)
    # birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=100, default='author')  # Added field

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def age(self):
        import datetime
        return datetime.datetime.now().year - self.birth_year if self.birth_year else None

    def __str__(self):
        return self.full_name
    
############################################################  UPLOAD  ###################################################################

from django.db import models
# from .views import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    cover_page = models.ImageField(upload_to='covers/')  # New field for cover image
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')])
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_published = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def _str_(self):
        return self.title

    def delete_file(self):
        # Delete the associated file and cover page
        if self.file:
            self.file.delete(save=False)
        if self.cover_page:
            self.cover_page.delete(save=False)
        self.delete()  # Delete the Book object itself

