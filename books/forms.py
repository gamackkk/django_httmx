from django.forms import ModelForm, TextInput, CharField
from .models import Book
from django.utils.translation import gettext_lazy as _

class BookCreateForm(ModelForm):
    title = CharField(required=True, widget=TextInput(attrs={'class': 'clrtxt', 'placeholder': _('Title')}))
    author = CharField(required=True, widget=TextInput(attrs={'class': 'clrtxt', 'placeholder': _('Author')}))
    price = CharField(required=True, widget=TextInput(attrs={'class': 'clrtxt', 'placeholder': _('Price')}))

    class Meta:
        model = Book
        fields = ['title','author','price']
class BookEditForm(BookCreateForm):
    title = CharField(required=True, widget=TextInput(attrs={"class":"form-control-sm form-control"}))
    author = CharField(required=True, widget=TextInput(attrs={"class":"form-control-sm form-control"}))
    price = CharField(required=True, widget=TextInput(attrs={"class":"form-control-sm form-control"}))
