from django.shortcuts import render,redirect,get_object_or_404
from.models import BookModel,BorrowBookModel,ReviewModel
from cetagories.models import CategoryModel
from django.views.generic import DetailView,UpdateView
from django.contrib import messages
from .forms import ReviewForm
from accounts.views import sending_user_mail
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request,category_slug=None):
    book = BookModel.objects.all()
    if category_slug is not None:
        category = CategoryModel.objects.get(slug = category_slug)
        book = BookModel.objects.filter(cetagory = category)
        
    category = CategoryModel.objects.all()
    return render(request,'home.html',{'book':book,'category':category})


class BookDetailView(DetailView):
    model = BookModel
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'
    context_object_name = 'book'

    def get_context_date(self,**kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = ReviewModel.objects.filter(book=book)
        return context


@login_required
def borrowBook(request,id):
    book = BookModel.objects.get(pk=id)
    user = request.user.account
    if request.method == 'POST':
        quantity = 1
        if quantity <= book.quantity and user.balance >= book.borrowing_price:
            BorrowBookModel.objects.create(user = request.user,book=book,quantity=quantity)
            book.quantity -= quantity
            book.save()
            user.balance -= book.borrowing_price
            user.save(
                update_fields = ['balance']
            )
            user.balance_after_transaction = user.balance
            user.save(update_fields=['balance_after_transaction'])

            sending_user_mail(request.user,'Borrowing Book','borrow_mail.html',book.borrowing_price)

            messages.success(request,'Borrowing book has been successfully')
            return redirect('book_details',id=book.id)
        else:
            messages.error(request,'You have no sufficient balance  / book has no quantity')
    
    return render(request,'book_details.html',{'book':book})


@login_required
def AddReview(request,id):
    book = BookModel.objects.get(pk=id)
    user = request.user
    borrowed_books = BorrowBookModel.objects.filter(user=user,book=book)

    if not borrowed_books.exists():
        messages.error(request, 'You can only review books if you borrowed.')
        return redirect('book_details', id=id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.book = book
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('book_details', id=id)
    else:
        form = ReviewForm()

    return render(request, 'review_form.html', {'form': form, 'book': book})


@login_required
def return_book(request, borrow_id):
    borrow_instance = get_object_or_404(BorrowBookModel, pk=borrow_id)
    user_account = request.user.account

    # Add borrowing price back to user's balance
    user_account.balance += borrow_instance.book.borrowing_price
    user_account.save(update_fields=['balance'])

    # Delete the BorrowBookModel instance
    borrow_instance.delete()

    sending_user_mail(request.user,'Retturn Book','return_book_mail.html',borrow_instance.book.borrowing_price)
    messages.success(request, 'Book returned successfully.')
    return redirect('profile')


