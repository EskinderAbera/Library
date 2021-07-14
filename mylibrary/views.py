from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . models import User, Author, Book
from . forms import FirstBookForm, SecondBookForm, ThirdBookForm

# Create your views here.
def index(request):
    return render(request, "mylibrary/index.html", {
        "Books": Book.objects.order_by('-createdAt')
    })


def book_detail(request, book_id):
    book = Book.objects.get(pk = book_id)
    return render(request, "mylibrary/book_detail.html", {
        "book":book
    })


def books_search_view(request):
    title = request.GET['title']
    books = Book.objects.filter(title__contains = title)
    if books:
        return render(request, "mylibrary/book_search_page.html", {
            "books": books
        }) 
    else:         
        return render(request, "mylibrary/error.html", {
        "message": "Book Does not exist!"
        })


def addbooks_view(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
        'tform':ThirdBookForm()
    }

    if request.method == 'POST':
        form = ThirdBookForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']             
            title = request.POST['title']
            author = Author.objects.get(pk = int(request.POST["author"]))
            publishDate = request.POST['publishDate']
            pageCount = request.POST['pageCount']
            description = request.POST['description']
            book = Book.objects.create( title = title,
                                    author = author,
                                    publishDate = publishDate,
                                    pageCount= pageCount,
                                    description=description,
                                    image = image
                                )
            return redirect('bookdetail', book.id)
        else:
            return render(request, "mylibrary.html/addbooks.html", {
                "form": form,
                "message": "Wrong Input!"
            })
    
    return render(request, "mylibrary/addbooks.html", context) 

    
def edit(request, book_id):
    book = Book.objects.get(pk = book_id)
    if request.method == 'POST':
        tform = ThirdBookForm(request.POST, request.FILES)
        if tform.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            pageCount = request.POST['pageCount']
            publishDate = request.POST['publishDate']
            image = tform.cleaned_data['image']
            author = Author.objects.get(pk = int(request.POST["author"]))

            bookCreated = Book.objects.create(
                title = title,
                description = description,
                publishDate = publishDate,
                pageCount = pageCount,
                image = image,
                author = author,
            )
                        
            return redirect('bookdetail', bookCreated.id)
        
    return render(request, "mylibrary/edit.html", {
        "tform": ThirdBookForm(instance= book),
        "book": book,
        "authors":Author.objects.all()
            })


def delete(request, book_id):  
    book = Book.objects.get(pk = book_id)  
    book.delete()  
    return redirect('index')


def delete_author(request, author_id):  
    author = Author.objects.get(pk = author_id)  
    author.delete()  
    return redirect('authors')


def add_author(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            author = Author.objects.get(first_name= first_name, last_name=last_name)
            return render(request, "mylibrary/add_author.html", {
                "message":"author exist!"})
        except Author.DoesNotExist:
            author = Author.objects.create(first_name=first_name, last_name=last_name)
            author.save()
            return HttpResponseRedirect(reverse("authors"))

    return render(request, "mylibrary/add_author.html")


def author_view(request, author_id):
    author = Author.objects.get(pk=author_id)
    books = Book.objects.filter(author=author)
    
    return render(request, "mylibrary/author.html", {
        "author":author,
        "books" : books
    })


def author_edit(request, author_id):
    author = Author.objects.get(pk = author_id)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        authorUpdated = Author.objects.update(
                first_name = first_name,
                last_name = last_name
            )
                        
        return redirect('authorview', author_id)  

        
    return render(request, "mylibrary/author_edit.html", {
        "author":author
    })


def authors_view(request):
    return render(request, "mylibrary/authors.html", {
        "authors": Author.objects.all()
    })


def search_view(request):
    first_name = request.GET['first_name']
    authors = Author.objects.filter(first_name__contains = first_name)
    if authors:
        return render(request, "mylibrary/search page.html", {
            "authors": authors
        }) 
    else:         
        return render(request, "mylibrary/error.html", {
        "message": "Author Does not exist!"
        })   


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mylibrary/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, "mylibrary/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mylibrary/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mylibrary/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, "mylibrary/register.html")


