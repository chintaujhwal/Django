from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Avg
from django.http import JsonResponse, HttpResponse
from .models import Book
from .forms import BookForm
from django.shortcuts import render, redirect
import datetime

def book_home(request):
    summary = Book.objects.all().aggregate(count=Count('id'), avg_price=Avg('price'))
    return render(request, 'home.html', {'summary': summary})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'list.html', {'books': books})


def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/books/list")
        else:
            return render(request, 'add.html', {'form': form, 'message': "Sorry! could not add the book"})
    else:
        form = BookForm()
        return render(request, 'add.html', {'form': form})


def book_edit(request, id):
    if request.method == 'GET':
        try:
            book = Book.objects.get(id=id)
            form = BookForm(instance=book)
            return render(request, 'edit.html', {'form': form})
        except ObjectDoesNotExist:
            return render(request, 'edit.html', {'message': "Book not found"})
    else:
        book = Book.objects.get(id=id)
        form = BookForm(instance=book, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/books/list")
        else:
            return render(request, 'edit.html', {'form': form})


def book_delete(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return redirect("/books/list")
    except ObjectDoesNotExist:
        return render(request, 'delete.html', {'message': " Book not found"})
    except Exception as ex:
        print(ex)
        return render(request, 'delete.html', {'message': " Book could not be deleted"})


def book_search(request):
    if 'search' in request.COOKIES:
        title = request.COOKIES['search']
    else:
        title = ''

    return render(request, 'search.html', {'title':title})


def book_dosearch(request):
    title = request.GET['title']
    books = list(Book.objects.filter(title__contains=title).values())

    response = JsonResponse(books, safe=False)
    response.set_cookie("search", title, expires=datetime.datetime.now() + datetime.timedelta(days=7))

    return response