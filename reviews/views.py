import os
from django.shortcuts import redirect, render, get_object_or_404
from .models import Book,Review,Contributor,BookContributor,Blog
from .utils import average_rating
from .forms import SearchForm,Registrationform,UpdateForm,UploadForm
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .ratings import ratingCalc
from django.contrib import messages

def index(request):
        book = Book.objects.all()
        contributor = Contributor.objects.all()
        featured = Book.objects.filter(featured = True)
        new_arrivals = Book.objects.order_by('-publication_date')[:8]
        blog = Blog.objects.all()
        context = {
            'book':book,
            'featured':featured,
            'new_arrivals':new_arrivals,
            'blog':blog
        }
        return render(request, "reviews/index.html",context)
    
def book_search(request):
    if request.method == 'GET':
        search_text = request.GET.get("q")
       
        if search_text:
        
            query = Book.objects.filter(title__icontains = search_text)
            return render(request,"reviews/search-results.html",{"search_text": search_text,"query": query})
    
        else:
            return render(request,'reviews/search-results.html',{"search_text": search_text})
    else:
            return render(request,'reviews/search-results.html')
    
        


def details(request,id):
    books = Book.objects.get(id=id)
    cont = books.book.all()
    allBooks = Book.objects.all().exclude(id=id)[:3]
    return render(request,'reviews/details.html',{'books':books,
                                                  'cont':cont,
                                                  'allBooks':allBooks})
    
@login_required
def userprofile(request,id):
    
    profile = request.user
    uploaded_books = Book.objects.filter(uploader=profile)
    book_count = Book.objects.filter(uploader=profile).count()
    context = {
        'profile':profile,
        'uploaded_books':uploaded_books,
        'book_count':book_count
    }
    return render(request,'reviews/profile.html',context)
    
def download(request,pk):
    
    instance = get_object_or_404(Book,pk=pk)
    
    if instance.file_field:
        file = instance.file_field.file
        response = FileResponse(file,content_type='application/pdf')
        
       
        response['Content-Disposition'] = f'attachment; filename="{instance.file_field.name}"'
        return response
    
    return HttpResponse("not found")

@login_required
def updateBook(request,id):
    book = Book.objects.get(id=id)
    if request.user != book.uploader:
        return redirect('profile')
    
    if request.method == 'POST':
       form = UpdateForm(request.POST,request.FILES, instance=book) 
       if form.is_valid():
           form.save()
           return redirect('profile')
     
    else:
       form = UpdateForm(instance=book) 
        
    
    return render(request,'reviews/update.html',{'form':form,'book':book})   
    
    
def BookDetails(request,book_id):
    books = Book.objects.get(id=book_id)
    
    
    return render(request,'reviews/bookdetails.html',{'books':books})

@login_required
def deleteBook(request,id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('profile')

@login_required
def uploadBook(request,user_id):
       
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploader = request.user
            book.save()
            return redirect('profile')
           
   
    else:
        
        form = UploadForm()
    
    return render(request,'reviews/upload.html',{'form':form})


def form_example(request):
    
    return render(request, "reviews/forms.html")


def loginform(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request,username=username,password=password)
    
    if user is not None:
        login(request,user)
        return redirect('index')
    else:
          
        return render(request,"reviews/login.html")
    
    return render(request, "reviews/login.html")
    
def registerform(request):
    if request.method == 'POST':
        form = Registrationform(request.POST)
    
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            login(request,user)
            
            return redirect('index')
    else:
            
            form = Registrationform()
        
  
        
    return render(request,'reviews/register.html', {'form':form})    
    
    


def logoutform(request):
    logout(request)
    return redirect('login')


def blogdetails(request,slug):
    blog = Blog.objects.get(id=slug)
    context = {
        'blog':blog
    }
    
    return render(request, 'reviews/blog.html',context)
    

#rating = [4,5,3,5,2]

#percentage_rating = ratingCalc(rating)
#print(percentage_rating)