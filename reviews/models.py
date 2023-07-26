from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Profile(models.Model):
    profileImage = models.ImageField(default='',upload_to='profile/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user
        
class Publisher(models.Model):
    
    """ A company that publishes books. """

    name = models.CharField(max_length=50,help_text="The name of the Publisher.")
    website = models.URLField(
    help_text="The Publisher's website.")
    email = models.EmailField(help_text="The Publisher's email address.")
    
    def __str__(self):
        
        return self.name
     
    
    
class Book(models.Model):
    """A published book."""
    title = models.CharField(
        max_length=100, help_text="The title of the book.")
    publication_date = models.DateField(
        verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    cover = models.ImageField(upload_to='covers/',null=True)
    file_field = models.FileField(upload_to="files/",null=True,blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor', through="BookContributor")
    featured = models.BooleanField(default=False)
    uploader = models.ForeignKey(User,on_delete=models.CASCADE, default='',null=True)
    date_uploaded = models.DateField(auto_now_add=True, null= True)
    
    
    

    def __str__ (self):
        return self.title


class Contributor(models.Model):
    """A contributor to a Book, e.g. author, editor,
    co-author."""
    first_names = models.CharField(
    max_length=50, help_text="The contributor's first name or names.")
    last_names = models.CharField(
    max_length=50, help_text="The contributor's last name or names.")
    email = models.EmailField(help_text="The contact email for the contributor.")
    
    def __str__ (self):
        return self.first_names + ' ' + self.last_names
    
class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,related_name='book')
    contributor = models.ForeignKey(
        Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor had in the book.", choices=ContributionRole.choices,
        max_length=20)
    
    
    def __str__(self):
        return str(self.contributor) + ' ' + self.role
        
    
class Review(models.Model):
    content = models.TextField(
help_text="The Review text.")
    rating = models.IntegerField(
help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(
auto_now_add=True,
help_text="The date and time the review was \
created.")
    
    date_edited = models.DateTimeField(
null=True, help_text="The date and time the review \
was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(
Book, on_delete=models.CASCADE,
    help_text="The Book that this review is for.")
    
    
    def __str__(self):
        
        return self.content
    class Meta:
        unique_together = ('book','creator')
        
        
class Blog(models.Model):
    title = models.CharField(max_length=250,help_text="Title of the Blog", verbose_name="Blog Title")
    contents = models.TextField(help_text="Blog contents" ,verbose_name="Blog Content")
    date_created = models.DateTimeField(auto_now=True, help_text="Date Created",verbose_name="Date Created")
    date_updated = models.DateTimeField(auto_now_add=True,help_text="Date Updated")
    images = models.ImageField(upload_to='Blog', help_text="Image of the Blog")
    user = models.ForeignKey(User, on_delete= models.CASCADE,help_text="The user who created The blog")
    slug = models.SlugField(unique=True, verbose_name="slug")
    
    class Meta:
        verbose_name_plural = 'Blog'
    
    def save(self,*args, **kwargs):
        
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    
    