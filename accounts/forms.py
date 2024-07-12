from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

##############################################################   UPLOAD  #################################################################

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'visibility', 'cost', 'year_published', 'file', 'cover_page']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and not file.name.lower().endswith(('.pdf', '.jpeg')):
            raise forms.ValidationError("File must be a PDF or JPEG.")
        return file

    def clean_cover_page(self):
        cover_page = self.cleaned_data.get('cover_page')
        if cover_page and not cover_page.name.lower().endswith('.jpeg'):
            raise forms.ValidationError("Cover page must be a JPEG.")
        return cover_page
