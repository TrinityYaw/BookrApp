from django.contrib import admin
from django.contrib.admin import AdminSite
from reviews.models import (Publisher, Contributor,Book, BookContributor, 
                            Review,Profile, Review, Blog)
from django.utils.text import slugify
# Register your models here.




class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn', 'publisher__name')
    list_display = ['title','publication_date','uploader','publisher','featured']
    list_filter = ('publisher', 'publication_date')
    date_hierarchy = 'publication_date'
    

class BookrAdminSite(AdminSite):
    title_header = 'Bookr Admin'
    site_header = 'Bookr administration'
    index_title = 'Bookr site admin'

admin_site = BookrAdminSite(name='bookr')

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
(None, {'fields': ('creator', 'book')}),
('Review content', {'fields': ('content',
'rating')}))
    list_display = ['book','rating','creator','content']

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('first_names','last_names')
    list_filter = ('last_names',)
    search_fields = ('first_names',)

class BookContributorAdmin(admin.ModelAdmin):
    list_display = ('book','contributor','role')
    
    
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','user']
    prepopulated_fields = {'slug': ('title',)}
    
    
    def save_model(self,request,obj,form,change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request,obj,form,change)
    

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Contributor,ContributorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookContributor,BookContributorAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Profile)
admin.site.register(Blog, BlogAdmin)
