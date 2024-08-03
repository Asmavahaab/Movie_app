from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_choices = [
        ('user', 'user'),
        ('admin', 'admin'),
    ]
    type = models.CharField(choices=type_choices,blank=True, null=True,max_length=5)
    # username = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=200)
    # last_name = models.CharField(max_length=200)
    # email = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    # confirm_password = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MovieDetails(models.Model):
    added_by = models.ForeignKey(User,on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="movie_image/")
    description = models.TextField(max_length=500)
    release_date = models.DateField()
    actors = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    YouTube_trailer_link = models.URLField()

class ReviewRating(models.Model):
    movie = models.ForeignKey(MovieDetails, on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rating_choices = [
        (1,'1 star'),
        (2, '2 star'),
        (3, '3 star'),
        (4, '4 star'),
        (5, '5 star'),
    ]
    rating = models.IntegerField(choices=rating_choices)
