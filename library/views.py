from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, MemberForm, BookForm, BookLendingForm, BookSearchForm
from .models import Book, Member, BookLending

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        member_form = MemberForm(request.POST)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        member_form = MemberForm()
    return render(request, 'library/register.html', {'user_form': user_form, 'member_form': member_form})

@login_required
def dashboard(request):
    try:
        member = request.user.member
        borrowed_books = member.get_borrowed_books()
        return render(request, 'library/dashboard.html', {
            'member': member,
            'borrowed_books': borrowed_books
        })
    except Member.DoesNotExist:
        return redirect('home')

def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        category = form.cleaned_data.get('category')
        availability = form.cleaned_data.get('availability')

        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )
        if category:
            books = books.filter(category=category)
        if availability:
            if availability == 'available':
                books = books.filter(available_quantity__gt=0)
            elif availability == 'unavailable':
                books = books.filter(available_quantity=0)

    return render(request, 'library/book_list.html', {'books': books, 'form': form})

@login_required
def book_create(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('book_list')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.available_quantity = book.quantity
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Create'})

@login_required
def book_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('book_list')

    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Update'})

@login_required
def book_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('book_list')

    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})

@login_required
def borrow_book(request):
    initial_book_id = request.GET.get('book')
    initial_data = {'book': initial_book_id} if initial_book_id else None
    
    if request.method == 'POST':
        form = BookLendingForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            
            # Check if user already has this book
            existing_lending = BookLending.objects.filter(
                book=book,
                member=request.user.member,
                returned_date__isnull=True
            ).exists()
            
            if existing_lending:
                messages.error(request, "You already have this book borrowed.")
                return redirect('dashboard')
            
            # Check if user has reached maximum allowed books (e.g., 3 books)
            current_borrows = BookLending.objects.filter(
                member=request.user.member,
                returned_date__isnull=True
            ).count()
            
            if current_borrows >= 3:
                messages.error(request, "You can't borrow more than 3 books at a time.")
                return redirect('dashboard')
            
            # Check if user has any overdue books
            if request.user.member.has_overdue_books():
                messages.error(request, "You have overdue books. Please return them before borrowing new ones.")
                return redirect('dashboard')
            
            lending = form.save(commit=False)
            lending.member = request.user.member
            lending.save()
            
            # Update book's available quantity
            book.available_quantity -= 1
            book.save()
            
            # Send email notification
            subject = 'Book Borrowed Successfully'
            message = f'''You have borrowed "{lending.book.title}" by {lending.book.author}.
            Due date: {lending.due_date.strftime('%B %d, %Y')}
            
            Please return the book on time to avoid fines.
            Current fine rate: $1 per day overdue.'''
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])
            
            messages.success(request, f'Successfully borrowed "{lending.book.title}".')
            return redirect('dashboard')
    else:
        form = BookLendingForm(initial=initial_data)
        
        # Get all books that are currently borrowed by the user
        borrowed_books = set(BookLending.objects.filter(
            member=request.user.member,
            returned_date__isnull=True
        ).values_list('book_id', flat=True))
        
        # Get all available books
        available_books = Book.objects.filter(available_quantity__gt=0)
        
        # Exclude borrowed books from the queryset
        available_books = [book for book in available_books if book.id not in borrowed_books]
        
        # Update the form's queryset
        form.fields['book'].queryset = Book.objects.filter(id__in=[book.id for book in available_books])

    return render(request, 'library/borrow_book.html', {
        'form': form,
        'current_borrows': BookLending.objects.filter(
            member=request.user.member,
            returned_date__isnull=True
        ),
        'max_allowed': 3
    })

@login_required
def return_book(request, lending_id):
    lending = get_object_or_404(BookLending, id=lending_id, member=request.user.member)
    if request.method == 'POST':
        lending.return_book()
        
        # Send email notification
        subject = 'Book Returned Successfully'
        message = f'You have returned {lending.book.title}. Fine amount: ${lending.fine_amount}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])
        
        return redirect('dashboard')
    return render(request, 'library/return_book.html', {'lending': lending})
