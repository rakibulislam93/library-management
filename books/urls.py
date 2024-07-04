from django.urls import path
from .views import home,BookDetailView,borrowBook,AddReview,return_book
urlpatterns = [
    path('',home,name='homepage'),
    path('category/<slug:category_slug>/',home,name='category_wise_book'),
    path('book_details/<int:id>/',BookDetailView.as_view(),name='book_details'),
    path('borrow_book/<int:id>/',borrowBook,name='borrow_book'),
    path('add_review/<int:id>',AddReview,name='book_review'),
    path('return_book/<int:borrow_id>/', return_book, name='return_book'),
    
]
