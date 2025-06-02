from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Member, BookLending

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('phone_number', 'address')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'isbn', 'category', 'description', 'quantity')

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        return quantity

class BookLendingForm(forms.ModelForm):
    class Meta:
        model = BookLending
        fields = ('book', 'member')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(available_quantity__gt=0)

class BookSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search')
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Book.CATEGORY_CHOICES
    )
    availability = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All'),
            ('available', 'Available'),
            ('unavailable', 'Unavailable')
        ]
    ) 