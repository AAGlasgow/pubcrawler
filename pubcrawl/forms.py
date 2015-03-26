from django import forms
from pubcrawl.models import Page, Category, UserProfile, Review, Crawl
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class ReviewForm(forms.ModelForm):
    text = forms.CharField(max_length=750, help_text="Enter your review here...", widget=forms.Textarea)
    class Meta:
        model = Review
        fields = ('text',)

class CrawlForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Name of the crawl: ")
    drink = forms.BooleanField(initial=False, help_text="Drink?")
    drinkDescription = forms.CharField(max_length=500, help_text="description")
    costume = forms.BooleanField(initial=False, help_text="Cotume?")
    costumeDescription = forms.CharField(max_length=500, help_text="description")
    description = forms.CharField(max_length=500,help_text="Crawl desciption: ")
    picture = forms.ImageField(help_text="Upload a picture", required=False)
    class Meta:
        model = Crawl
        fields = ('name', 'drink', 'drinkDescription', 'costume', 'costumeDescription', 'description', 'picture',)