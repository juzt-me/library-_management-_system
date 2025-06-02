from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='library/login.html'), name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/<int:lending_id>/', views.return_book, name='return_book'),
] 