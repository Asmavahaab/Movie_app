from django import forms
from django.contrib.auth.models import User
from .models import *

class update_user_details_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class user_details_form(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['type']

class category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class movie_details_form(forms.ModelForm):
    class Meta:
        model = MovieDetails
        fields = ['movie_title', 'poster', 'description', 'release_date', 'actors', 'category', 'YouTube_trailer_link']

class review_rating_form(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review', 'rating']