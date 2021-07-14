from django import forms
from django.forms import widgets
from django.forms.widgets import Widget
from . models import Book, Author

class FirstBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author')
        widgets = {
                   'title': forms.TextInput(attrs={'class': 'form-item'}),
                   'author' : forms.Select(choices=Author.objects.all(), attrs={'class' : 'form-item'})
                   } 

class SecondBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('publishDate', 'pageCount')
        widgets = {
                   'publishDate': forms.DateInput(attrs={'class': 'form-item'}),
                   'pageCount': forms.NumberInput(attrs={'class': 'form-item'})
                   } 


class ThirdBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('image',)
        widgets = {
                'image': forms.FileInput(attrs={'class': 'book-cover filepond'})
        }        

class UpdateForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Book
        fields = ('title', 'description','pageCount', 'publishDate', 'image', 'author')
        widgets = {
            'publishDate': forms.DateInput(attrs={'type':'date'})
            }