
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from .models import CustomUser
from .models import Book
from .forms import CustomAuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def index(request):
    files = Book.objects.all()  # Fetch all uploaded books
    context = {
        'files': files,
    }
    context['full_name'] = request.user.full_name
    return render(request, 'index.html', {'files': files})


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        state = request.POST.get('state')
        address = request.POST.get('address')
        public_visibility = request.POST.get('public_visibility')
        user_type = request.POST.get('user_type')

        if password1 == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'register.html')
            else:
                user = CustomUser.objects.create_user(email=email, password=password1)
                user.full_name = full_name
                user.gender = gender
                user.city = city
                user.state = state
                user.address = address
                user.public_visibility = (public_visibility == 'True')
                user.user_type = user_type
                user.save()
                
                subject = 'Email confirmation for social_book'
                message = 'Congratulation on successful registeration.Welcome to social book community!!'
                from_email = 'admin@social_book.com'  # Replace with your email
                recipient_list = [email]  # Replace with recipient email

                send_mail(subject, message, from_email, recipient_list)
                
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' field actually holds the email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                django_login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


# @api_view(['POST'])
# def logout_view(request):
#     if request.method=='POST':
#         request.user.auth.token.detele()
#         return Response(status=status.HTTP_200_OK)
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect

def logout(request):
    django_logout(request)
    return redirect('login')


def authorseller(request):
    if request.method == 'POST':
        visibility = request.POST.get('visibility', 'default')
        user_type_filter = request.POST.get('user_type_filter', 'all')  # Assuming you have a filter for user type

        try:
            if visibility == 'public':
                if user_type_filter == 'author':
                    users = CustomUser.objects.filter(public_visibility=True, user_type='author')
                elif user_type_filter == 'seller':
                    users = CustomUser.objects.filter(public_visibility=True, user_type='seller')
                else:
                    users = CustomUser.objects.filter(public_visibility=True)
            elif visibility == 'private':
                if user_type_filter == 'author':
                    users = CustomUser.objects.filter(public_visibility=False, user_type='author')
                elif user_type_filter == 'seller':
                    users = CustomUser.objects.filter(public_visibility=False, user_type='seller')
                else:
                    users = CustomUser.objects.filter(public_visibility=False)
            else:
                if user_type_filter == 'author':
                    users = CustomUser.objects.filter(user_type='author')
                elif user_type_filter == 'seller':
                    users = CustomUser.objects.filter(user_type='seller')
                else:
                    users = CustomUser.objects.all()

            context = {'users': users}
            return render(request, 'authorseller.html', context)
        except Exception as e:
            # Handle the exception, e.g., log the error, display a message to the user, etc.
            error_message = f"An error occurred: {str(e)}"
            context = {'error_message': error_message}
            return render(request, 'authorseller.html', context)
    else:
        # Handle the case if the request method is not POST
        error_message = "Invalid request method. Please use POST method."
        context = {'error_message': error_message}
        return render(request, 'authorseller.html', context)



#################################################################   UPLOAD    ##############################################################

# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Book
# from django.contrib.auth import get_user_model
from .forms import BookForm
from django.contrib import messages
from django.http import HttpResponse
from .serializers import BookSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth.decorators import login_required
from .decorators import check_uploaded_files
from rest_framework.authtoken.models import Token
import os
from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from django.conf import settings
from.serializers import *
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
import requests

# User=get_user_model()
users=CustomUser.objects.all()
for user in users:
#    token= Token.objects.get_or_create(user=user)
   token, created = Token.objects.get_or_create(user=user)
   print(token)

def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('upload')
    else:
        form = BookForm()
    files = Book.objects.filter(uploaded_by=request.user)
    return render(request, 'upload.html', {'form': form, 'files': files})


# def upload_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'File uploaded successfully!')
#             return redirect('upload')
#     else:
#         form = BookForm()
#     files = Book.objects.all()
#     return render(request, 'upload.html', {'form': form, 'files': files})

def delete_uploaded_file(request, book_id): #file_id
    file = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        file.delete()
        messages.success(request, 'File deleted successfully!')
    return redirect('upload')



def view_uploaded_file(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'view.html', {'book': book})



def already_uploaded(request):
    email = request.GET.get('username') # username is where the email variable is getting stored
    files =Book.objects.all()
    if email:
        try:
            user = CustomUser.objects.get(email=email)
            files = Book.objects.filter(uploaded_by = user)
        except CustomUser.DoesNotExist:
            files = []
    else:
        #files = Book.objects.filter(uploaded_by=request.user)
        files = Book.objects.all()
    #users = CustomUser.objects.all()

    return render (request, 'already_uploaded.html', {'files':files})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uploaded_files(request):
    user = request.user
    files = Book.objects.filter(uploaded_by=user)
    serializer = BookSerializer(files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
@check_uploaded_files
def my_books(request):
    files = Book.objects.filter(uploaded_by=request.user)
    return render(request, 'my_books.html', {'files': files})

class UserUploadedFilesView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(uploaded_by=self.request.user)

class ServeFileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, book_id):#file_id
        file = get_object_or_404(Book, id=book_id, uploaded_by=request.user)  # Ensure the file belongs to the user
        file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
        if not os.path.exists(file_path):
            raise Http404("File does not exist")

        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        except Exception as e:
            raise Http404("Error reading file: " + str(e))
        
  