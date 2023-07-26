from django import forms
from django.contrib.auth.models import User
from .models import Book


class SearchForm(forms.Form):
    Choices = (
        ('Title','Title'),
        ('ISBN','ISBN'),
        ('Contributor','Contributor')
    )
    
    search_options = forms.ChoiceField(choices = Choices)
    
class Registrationform(forms.Form):
   username = forms.CharField(max_length=50, required=False,widget=forms.TextInput(attrs={'class':'form form-control form-floating'}))
   email = forms.EmailField(max_length=50, required=False,widget=forms.TextInput(attrs={'class':'form form-control form-floating'}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form form-control form-floating'}))
   confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form form-control form-floating'}))
   
   
   def clean(self):
       cleaned_data = super().clean()
       password = cleaned_data.get('password')
       confirm_password = cleaned_data.get('confirm_password')
       
       if password and confirm_password and password != confirm_password:
           raise forms.ValidationError("passwords do not match")
       
   def save(self):
       username = self.cleaned_data.get('username')
       email = self.cleaned_data.get('email')
       password = self.cleaned_data.get('password')
       
       user = User.objects.create_user(username=username,email=email,password=password)
       
       
       return user

       

class UpdateForm(forms.ModelForm):
        
       
       class Meta:
           model = Book
           fields = ("title","publication_date","isbn","cover","file_field","publisher")
           
           
class UploadForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ("title","publication_date","isbn","cover","file_field","publisher")
        
           
           
   

