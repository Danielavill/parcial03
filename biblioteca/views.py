from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('books')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def books(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'books.html', {"books": books})

@login_required
def books_completed(request):
    books = Book.objects.filter(user=request.user, created__isnull=False).order_by('-created')
    return render(request, 'books.html', {"books": books})


@login_required
def create_book(request):
    if request.method == "GET":
        return render(request, 'create_book.html', {"form": BookForm})
    else:
        try:
            form = BookForm(request.POST, request.FILES)
            new_book = form.save(commit=False)
            new_book.user = request.user
            new_book.save()
            return redirect('books')  
        except ValueError:
            return render(request, 'create_book.html', {"form": BookForm, "error": "Error creating book."})


def home(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'home.html', context)


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('books')

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id, user=request.user)
    if request.method == 'GET':
        form = BookForm(instance=book)
        return render(request, 'book_detail.html', {'book': book, 'form': form})
    else:
        try:
            form = BookForm(request.POST, request.FILES, instance=book)
            form.save()
            return redirect('books') 
        except ValueError:
            return render(request, 'book_detail.html', {'book': book, 'form': form, 'error': 'Error updating book.'})

@login_required
def complete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id, user=request.user)
    if request.method == 'POST':
        book.datecompleted = timezone.now()
        book.save()
        return redirect('books') 

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('books')  