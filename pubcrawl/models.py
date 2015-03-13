from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
        name = models.CharField(max_length=128, unique=True)
        views = models.IntegerField(default=0)
        likes = models.IntegerField(default=0)
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

class Pub(models.Model):
        link = models.URLField(unique=True)
        name = models.CharField(max_length=128)
        def save(self, *args, **kwargs):
                super(Pub, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

class Crawl(models.Model):
        creator = models.ForeignKey(User)
        name = models.CharField(max_length=128)
        pubs = models.ManyToManyField(Pub)
        slug = models.SlugField(unique=True)
        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Crawl, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

class Review(models.Model):
        user = models.ForeignKey(User)
        crawl = models.ForeignKey(Crawl)
        raiting = models.IntegerField(default=0) #0-5 Stars
        text = models.CharField(max_length=750)
        def save(self, *args, **kwargs):
                super(Review, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.text






