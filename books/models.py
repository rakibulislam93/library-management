from django.db import models
from cetagories.models import CategoryModel
from django.contrib.auth.models import User

# Create your models here.

class BookModel(models.Model):
    cetagory = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,related_name='category')
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrowing_price = models.DecimalField(max_digits=12,decimal_places=2)
    image = models.ImageField(upload_to='books/media/uploads',blank=True,null=True)
    quantity = models.PositiveIntegerField(null=True,default=0)

    def __str__(self) -> str:
        return self.title
    

class BorrowBookModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='borrow')
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE,related_name='borrow')
    quantity = models.PositiveIntegerField()
    borrow_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username
    


class ReviewModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=100)
    body = models.TextField()
    rating = models.IntegerField()
    review_date = models.DateTimeField(auto_now_add=True)