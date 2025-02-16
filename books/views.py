from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from .forms import BookCreateForm, BookEditForm
from .models import Book
from django.views.decorators.http import require_http_methods
from django.core.cache import cache


def delete_cache_keys():
    key_list = ['cached_book_list']
    for col in ('pk', 'title', 'author', 'price', 'read'):
        key_list += ['cached_book_list_sorted_' + col]
        key_list += ['cached_book_list_sorted_-' + col]
    cache.delete_many(key_list)


@require_http_methods(['GET'])
def book_list(request):
    book_list = cache.get_or_set('cached_book_list', Book.objects.all(), 60*5)  # Cache for 5 minutes
    form = BookCreateForm(auto_id=False)
    return render(request, 'base.html', {'book_list': book_list, 'form': form})

@require_http_methods(['POST'])
def create_book(request):
    form = BookCreateForm(request.POST)
    if form.is_valid():
        book = form.save()
        delete_cache_keys()
        return render(request, 'partial_book_detail.html', {'book': book})
    else:
        return render(request, 'partial_create_book_form.html', {'form': form}, status=422)

def update_book_details(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookEditForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            delete_cache_keys()
            return render(request, 'partial_book_detail.html', {'book': book})
        else:
            status = 422
    else:
        form = BookEditForm(instance=book)
        status = 200
    return render(request, 'partial_book_update_form.html', {'book': book, 'form': form}, status=status)

@require_http_methods(['GET'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'partial_book_detail.html', {'book': book})

@require_http_methods(['DELETE'])
def delete_book(request, pk):
    book = get_object_or_404(Book,pk=pk)
    delete_cache_keys()
    cache.delete('cached_book_list')  # Delete cache when a book is deleted
    return HttpResponse()
@require_http_methods(['PATCH'])
def update_book_status(request,pk):
    book = get_object_or_404(Book,pk=pk)
    book.read = not book.read
    book.save()
    delete_cache_keys()
    return render(request, 'partial_book_detail.html', {'book': book})

@require_http_methods(['GET'])
def book_list_sort(request, filter, direction):
    filter_dict = {_('id'): 'pk',
                   _('title'): 'title',
                   _('author'): 'author',
                   _('price'): 'price',
                   _('read'): 'read'}

    if filter in filter_dict:
        sort_str = ('-', '')[direction == _('ascend')] + filter_dict[filter]
        cache_key = 'cached_book_list_sorted_' + sort_str
        book_list = cache.get_or_set(cache_key, Book.objects.order_by(sort_str))
    else:
        book_list = cache.get_or_set('cached_book_list', Book.objects.all())

    return render(request, 'partial_book_list.html', {'book_list': book_list})
