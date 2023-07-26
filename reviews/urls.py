from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('search/',views.book_search, name="search"),
    path('details/<int:id>/',views.details, name="details"),
    path('download-pdf/<int:pk>/',views.download, name="download_pdf"),

    path('form/',views.form_example, name="form_example"),
    path('profile/<int:id>/',views.userprofile, name="profile"),
    path('profile/details/<int:book_id>/',views.BookDetails ,name="book_details"),
    path('profile/delete/<int:id>',views.deleteBook, name="delete"),
    path('profile/update/<int:id>',views.updateBook, name="update"),
    path('profile/upload/<int:user_id>',views.uploadBook, name="upload"),
    path('blog/<slug:slug>', views.blogdetails,name ="blog"),
    
    path('login/',views.loginform, name="login"),
    path('register/',views.registerform, name="register"),
    
    path('logout',views.logoutform, name="logout"),
    
]
