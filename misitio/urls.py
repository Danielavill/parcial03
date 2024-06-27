"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from biblioteca import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('books/', views.books, name='books'),  # Cambio de 'tasks' a 'books'
    path('books_completed/', views.books_completed, name='books_completed'),  # Cambio de 'tasks_completed' a 'books_completed'
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_book/', views.create_book, name='create_book'),  # Cambio de 'create_task' a 'create_book'
    path('books/<int:book_id>', views.book_detail, name='book_detail'),  # Cambio de 'tasks/<int:task_id>' a 'books/<int:book_id>'
    path('books/<int:book_id>/delete', views.delete_book, name='delete_book'),  # Cambio de 'tasks/<int:task_id>/delete' a 'books/<int:book_id>/delete'
    path('books/<int:book_id>/complete/', views.complete_book, name='complete_book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
