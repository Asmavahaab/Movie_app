from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('password1')
        type = request.POST.get('type')

        admin_password = 'admin'

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This mail ID already exists')
                return redirect('register')
            else:
                if type == 'admin' and password != admin_password:
                    messages.error(request, "You cannot register as an admin without the correct admin password")
                    return redirect('register')
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                UserDetails.objects.create(user=user, type=type)

            return redirect('login')
        else:
            messages.info(request, "The password doesn't match")
            return redirect('register')
        return redirect('login')
    return render(request, 'register.html')

def update_user_details(request):
    if request.method == 'POST':
        form = update_user_details_form(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'User details updated successfully')
            user_details = UserDetails.objects.get(user=request.user)
            ty_pe = user_details.type
            if ty_pe == 'user':
                return redirect('user_home')
            elif ty_pe == 'admin':
                return redirect('admin_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form=update_user_details_form(instance=request.user)
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'
    return render(request,'update_user.html',{'form':form,'cancel_url':cancel_url})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            try:
                user_details = UserDetails.objects.get(user=user)
                ty_pe = user_details.type

                if ty_pe == 'user':

                    return redirect('user_home')
                elif ty_pe == 'admin':
                    return redirect('admin_home')
            except UserDetails.DoesNotExist:
                messages.error(request, 'User details not found. Please contact support.')
                return redirect('login')


        else:
            messages.info(request, 'Invalid Credentials...')
            print('asma')
            return redirect('login')
    return render(request, 'login.html')

def logOut(request):
    auth.logout(request)
    return redirect('login')


def user_home_page(request):
    if not hasattr(request.user, 'userdetails') or request.user.userdetails.type != 'user':
        messages.error(request, 'You do not have permission to access this USER page.')
        return redirect('login')
    if request.user.is_authenticated:
        movies = MovieDetails.objects.all()
        categories = Category.objects.all()
        ratings = ReviewRating.objects.all()

        movies_by_category = {}

        for category in categories:
            movies_by_category[category] = movies.filter(category=category)

        context = {
            'movies': movies,
            'movies_by_category' : movies_by_category,
            'categories' : categories,
            'ratings' : ratings
        }
        return render(request, 'user_home.html', context)
    else:
        return redirect('login')


def admin_home_page(request):
    if not hasattr(request.user, 'userdetails') or request.user.userdetails.type != 'admin':
        messages.error(request, 'You do not have permission to access this ADMIN page.')
        return redirect('login')

    if request.user.is_authenticated:
        movies = MovieDetails.objects.all()
        categories = Category.objects.all()
        ratings = ReviewRating.objects.all()

        movies_by_category = {}

        for category in categories:
            movies_by_category[category] = movies.filter(category=category)

        admin = UserDetails.objects.filter(type='admin')
        users = UserDetails.objects.filter(type='user')


        context = {
            'movies': movies,
            'categories' : categories,
            'movies_by_category': movies_by_category,
            'admin' : admin,
            'users' : users,
            'ratings' :ratings
        }
        return render(request, 'admin_home.html', context)
    else:
        return redirect('login')


        form = update_user_form(instance=request.user)

    return render(request, 'update_user.html', {'form': form})


def update_user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was updated successfully.')
            user_details = UserDetails.objects.get(user=request.user)
            ty_pe = user_details.type
            if ty_pe == 'user':
                return redirect('user_home')
            elif ty_pe == 'admin':
                return redirect('admin_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'

    return render(request, 'update_user_password.html', {'form': form,'cancel_url':cancel_url})


def add_movie(request):
    movie = MovieDetails.objects.all()
    if request.method == 'POST':
        form = movie_details_form(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully')
            user_details = UserDetails.objects.get(user=request.user)
            ty_pe = user_details.type
            if ty_pe == 'user':
                print('user entered')
                return redirect('user_home')
            elif ty_pe == 'admin':
                return redirect('admin_home')
    else:
        form = movie_details_form()
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'
    return render(request, 'add_movie.html', {'form': form, 'movie': movie,'cancel_url':cancel_url})


def update_movie(request, movie_id):
    movie = get_object_or_404(MovieDetails, id=movie_id)
    if not (request.user.is_authenticated and
            (request.user.userdetails.type == 'admin' or movie.added_by == request.user)):
        messages.error(request, 'You do not have permission to update this movie.')

    if request.method == 'POST':
        form = movie_details_form(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie.save()
            messages.success(request, 'Movie updated successfully!')
            user_details = UserDetails.objects.get(user=request.user)
            ty_pe = user_details.type
            if ty_pe == 'user':
                return redirect('user_home')
            elif ty_pe == 'admin':
                return redirect('admin_home')
    else:
        form = movie_details_form(instance=movie)
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'
    return render(request, 'update_movie.html', {'form': form,'cancel_url':cancel_url})

def delete_movie(request, movie_id):
    movie = get_object_or_404(MovieDetails, id=movie_id)
    if request.method == 'POST':
        movie.delete()
        user_details = UserDetails.objects.get(user=request.user)
        ty_pe = user_details.type
        if ty_pe == 'user':
            return redirect('user_home')
        elif ty_pe == 'admin':
            return redirect('admin_home')
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'

    context = {
        'movie': movie,
        'cancel_url': cancel_url
    }
    return render(request, 'delete_movie.html', context)

def add_category(request):
    if request.method == 'POST':
        form = category_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
            return redirect('admin_home')
    else:
        form = category_form()
    return render(request, 'add_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_home')
    context = {
        'category': category,
    }
    return render(request, 'delete_category.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(UserDetails, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_home')
    context = {
        'user': user,
    }
    return render(request, 'delete_user.html', context)


def search_movie(request):
    query = None
    movies = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movies = MovieDetails.objects.filter(Q(movie_title__icontains = query) | Q(category__name__icontains = query))
    else:
        movies = []
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'
    ratings = ReviewRating.objects.all()
    context = {
        'movies' : movies,
        'query' : query,
        'cancel_url' : cancel_url,
        'ratings' : ratings
    }
    return render(request,'search.html',context)

def add_rating_review(request,movie_id):
    movie = get_object_or_404(MovieDetails, id=movie_id)
    if request.method == 'POST':
        form = review_rating_form(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.save()
            messages.success(request, 'Rating added successfully!')
            user_details = UserDetails.objects.get(user=request.user)
            ty_pe = user_details.type
            if ty_pe == 'user':
                return redirect('user_home')
            elif ty_pe == 'admin':
                return redirect('admin_home')
    else:
        form = review_rating_form()
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'
    return render(request, 'add_rating.html', {'form': form,'cancel_url':cancel_url})

def delete_rating_review(request,rating_id):
    ratings = get_object_or_404(ReviewRating, id=rating_id)
    if request.method == 'POST':
        ratings.delete()
        user_details = UserDetails.objects.get(user=request.user)
        ty_pe = user_details.type
        if ty_pe == 'user':
            return redirect('user_home')
        elif ty_pe == 'admin':
            return redirect('admin_home')
    if hasattr(request.user, 'userdetails') and request.user.userdetails.type == 'admin':
        cancel_url = 'admin_home'
    else:
        cancel_url = 'user_home'

    context = {
        'ratings': ratings,
        'cancel_url': cancel_url
    }
    return render(request, 'delete_rating.html', context)
