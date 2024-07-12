# accounts/decorators.py
from django.shortcuts import redirect
from .models import Book

def check_uploaded_files(function):
    def wrap(request, *args, **kwargs):
        if Book.objects.filter(uploaded_by=request.user).exists():
            return function(request, *args, **kwargs)
        else:
            return redirect('upload')
    return wrap