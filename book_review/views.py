from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def register(request): 
    if request.method == "POST": 
        errors = User.objects.Registration_Validator(request.POST) 
        if len(errors) != 0: 
            for key, value in errors.items(): 
                messages.error(request, value) 
            return redirect('/') 
        else: 
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 
            new_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email = request.POST['email'], password = hashed_pw) 
            request.session['user_id'] = new_user.id 
            return redirect('/books')  
    return redirect('/')

def login(request): 
    if request.method == "POST": 
        errors = User.objects.Login_Validator(request.POST) 
    if len(errors) > 0: 
        for key, value in errors.items(): 
            messages.error(request, value) 
    return redirect('/') 
    this_user = User.objects.filter(email = request.POST['email']) 
    request.session['user_id'] = this_user[0].id 
    return redirect('/books') 
    return redirect('/')

def books(request): 
    if 'user_id' not in request.session: 
        return redirect('/') 
    this_user = User.objects.filter(id=request.session['user_id']) 
    context = { 
        'user': this_user[0], 
        'books': Book.objects.all(), 
        'recent_reviews': Review.objects.order_by('created_at').reverse()[0:3] 
    } 
    return render(request, 'books.html', context)

def add(request): 
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'bookReview.html', context)

def create(request): 
    if request.method == "POST": 
        user = User.objects.get(id=request.session['user_id']) 
        author = Author.objects.create(name=request.POST['new_author']) 
        book = Book.objects.create(title=request.POST['title'], author = author) 
        review = Review.objects.create(description=request.POST['review'], rating = request.POST['rating'], user = user, book = book) 
        return redirect(f'/books/{book.id}')

def add_review(request, book_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id']) 
        review = Review.objects.create(description=request.POST['review'], rating = request.POST['rating'], user = user, book = Book.objects.get(id=book_id))
        return redirect(f'/books/{book_id}')

def book(request, book_id): 
    context = { 
        'book': Book.objects.get(id=book_id) 
    } 
    return render(request, 'book.html', context)

def user(request, user_id): 
    context = {
        'user': User.objects.get(id=user_id), 
        'reviews': Review.objects.filter(user = user_id)
    }
    return render(request, 'user.html', context)

def delete(request, book_id, review_id):
    book = Book.objects.get(id=book_id)
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect(f'/books/{book_id}')

def logout(request): 
    request.session.flush() 
    return redirect('/')
