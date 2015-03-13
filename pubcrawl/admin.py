from django.contrib import admin
from pubcrawl.models import Category, Page
from pubcrawl.models import UserProfile

admin.site.register(UserProfile)



class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Update the registeration 
admin.site.register(Category, CategoryAdmin)



# Register your models here.
