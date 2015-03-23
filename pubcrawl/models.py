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
        placeID = models.CharField(max_length=256, unique=True)
        name = models.CharField(max_length=128)

        def __unicode__(self):
                return self.name

class Crawl(models.Model):
        creator = models.ForeignKey(User)
        positionCounter = 0
        name = models.CharField(max_length=128)
        drink = models.BooleanField(default=False)
        drinkDescription = models.CharField(max_length=500)
        costume = models.BooleanField(default=False)
        costumeDescription = models.CharField(max_length=500)
        description = models.CharField(max_length=500)
        picture = models.ImageField(upload_to='crawl_images', blank=True)
        dateTime = models.DateTimeField(auto_now=True)
        slug = models.SlugField(unique=True)
        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Crawl, self).save(*args, **kwargs)

        def add_pub(self, pub):
            self.positionCounter=self.positionCounter+1
            c_p = Crawl_Pub(pub=pub, crawl=self, position=self.positionCounter)
            c_p.save()
            return c_p

        def __unicode__(self):
                return self.name

class Crawl_Pub(models.Model):
    pub = models.ForeignKey(Pub)
    crawl = models.ForeignKey(Crawl)
    position = models.IntegerField()
    def __unicode__(self):
        return self.crawl.__unicode__()+" "+self.pub.__unicode__()+" Position: "+unicode(self.position)

class Review(models.Model):
        user = models.ForeignKey(User)
        crawl = models.ForeignKey(Crawl)
        liked = models.BooleanField(default=False)
        text = models.CharField(max_length=750)

        def __unicode__(self):
                return self.text






