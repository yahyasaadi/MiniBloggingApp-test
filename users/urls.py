from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.BlogList.as_view(), name='all-blogs'),
    path('blogs/<int:id>/', views.BlogDetail.as_view(), name='blog-detail'),
    path('blogs/new_blog/', views.CreateBlogView.as_view(), name='new-blog'),
    path('blogs/update/<int:id>/', views.UpdateBlogView.as_view(), name='update-blog'),
    path('blogs/delete/<int:id>/', views.DeleteBlogView.as_view(), name='delete-blog'), 

]