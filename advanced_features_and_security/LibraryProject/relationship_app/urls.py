from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # import the whole views module
from .views import list_books
urlpatterns = [
    # Books and Libraries
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    #path('logout/', LogoutView.as_view(next_page='login', allow_get=True), name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-Based Access Control
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

     # Book permissions
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]

