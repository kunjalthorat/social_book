from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('authorseller/', views.authorseller, name='authorseller'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('logout/', views.logout_view, name='logout'),  # Add this line
    
#########################################  UPLOAD  ###############################################

    path('upload/', views.upload_book, name='upload'),
    path('delete/<int:book_id>/', views.delete_uploaded_file, name='delete_uploaded_file'),
    path('view/<int:book_id>/', views.view_uploaded_file, name='view_uploaded_file'),
    path('already_uploaded/', views.already_uploaded, name='already_uploaded'),
    path('api/files/', views.get_uploaded_files, name='get_uploaded_files'),
    path('my_books/', views.my_books, name='my_books'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    