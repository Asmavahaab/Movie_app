from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name='register'),
    path('', views.login_user, name='login'),
    path('user_home/', views.user_home_page, name='user_home'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('admin_home/', views.admin_home_page,name='admin_home'),
    path('category/', views.add_category, name='add_category'),
    path('logout/', views.logOut,name='logout'),
    path('update_movie/<int:movie_id>/',views.update_movie,name='update_movie'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
    path('delete_movie/<int:movie_id>/',views.delete_movie, name='delete_movie'),
    path('delete_user/<int:user_id>/',views.delete_user, name='delete_user'),
    path('update_user',views.update_user_details,name='update_user'),
    path('update_user_password',views.update_user_password,name='update_user_password'),
    path('search/',views.search_movie,name='search'),
    path('add_rating_review/<int:movie_id>/',views.add_rating_review,name='add_rating'),
    path('delete_rating/<int:rating_id>/',views.delete_rating_review,name='delete_rating')
]