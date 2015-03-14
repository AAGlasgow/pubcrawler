import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from pubcrawl.models import Category, Page, Crawl, Pub, Review
from django.contrib.auth.models import User


def populate():

    butch_user = add_user('Butch', 'butch@gmail.com', 'myPassword')
    peter_user = add_user('Peter', 'peter@gmail.com', 'myPassword')
    rain_user = add_user('Rain', 'rain@gmail.com', 'myPassword')

    dram_pub = add_pub('DRAM!', 'ChIJKcWC6i1EiEgRrAN2HMyTv0U')
    nice_n_sleazy_pub = add_pub('Nice N Sleazy', 'ChIJ2U7jlChEiEgRaqr1lWpQ2RQ')
    curlers_rest_pub = add_pub('The Curlers Rest', 'ChIJCx0s8c5FiEgR1bZGWa3Jjik')
    guu_pub = add_pub('GUU', 'ChIJLd8s-c1FiEgRCl6u1MNHSNE')
    king_tuts_pub = add_pub('King Tuts Wah Wah Hut', 'ChIJD6VT8idEiEgRu0uJunEd8pc')
    buff_club_pub = add_pub('The Buff Club', 'ChIJRbplOSdEiEgR65ScWqJ11e8')

    get_pished_crawl = add_crawl(butch_user, 'Get Pished', [dram_pub, guu_pub, curlers_rest_pub])
    hippy_crawl_crawl = add_crawl(rain_user, 'Hippy Crawl', [king_tuts_pub, buff_club_pub, nice_n_sleazy_pub])

    hater_review = add_review(rain_user, get_pished_crawl, False, 'I didnt like it at all. There was no pub where anyone could sell me some weed or other drugs. Everyone else seemed to enjoy it though. Mainstream shite!')
    love_review = add_review(peter_user, get_pished_crawl, True, 'Was fucked that night, woke up the next day in my own sick somewhere in Dundee. Best night evaaa!')
    neutral_review = add_review(peter_user, hippy_crawl_crawl, True, 'Dont like all that drug taking shite. But thumb up cause its dead easy to pull those junky girls haha') 

    print "Users:"
    for u in User.objects.all():
        print u
    print ""
    print "Pubs:"
    for p in Pub.objects.all():
        print p
    print ""
    print "Crawls:"
    for c in Crawl.objects.all():
        print c
    print ""
    print "Reviews:"
    for r in Review.objects.all():
        print r

    

##    python_cat = add_cat('Python', 128, 64)
##
##    add_page(cat=python_cat,
##        title="Official Python Tutorial",
##        url="http://docs.python.org/2/tutorial/",
##        views=40)
##
##    add_page(cat=python_cat,
##        title="How to Think like a Computer Scientist",
##        url="http://www.greenteapress.com/thinkpython/",
##        views=40)
##
##    add_page(cat=python_cat,
##        title="Learn Python in 10 Minutes",
##        url="http://www.korokithakis.net/tutorials/python/",
##        views=48)
##
##    django_cat = add_cat("Django", 64, 32)
##
##    add_page(cat=django_cat,
##        title="Official Django Tutorial",
##        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/",
##        views=20)
##
##    add_page(cat=django_cat,
##        title="Django Rocks",
##        url="http://www.djangorocks.com/",
##        views=20)
##
##    add_page(cat=django_cat,
##        title="How to Tango with Django",
##        url="http://www.tangowithdjango.com/",
##        views=24)
##
##    frame_cat = add_cat("Other Frameworks", 32, 16)
##
##    add_page(cat=frame_cat,
##        title="Bottle",
##        url="http://bottlepy.org/docs/dev/",
##        views=16)
##
##    add_page(cat=frame_cat,
##        title="Flask",
##        url="http://flask.pocoo.org",
##        views=16)
##
##    my_cat = add_cat("David Froehlingsdorf", 200, 100)
##
##    add_page(cat=my_cat,
##        title="My Pythonanywhere page",
##        url="https://www.pythonanywhere.com/user/2079884FDavid/",
##        views=100)
##
##    add_page(cat=my_cat,
##        title="My Github page",
##        url="https://github.com/2079884FDavid/",
##        views=100)
##
##    # Print out what we have added to the user.
##    for c in Category.objects.all():
##        for p in Page.objects.filter(category=c):
##            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.views = views
    c.likes = likes
    return c

def add_user(name, email, password):
    u = User(username=name, email=email, password=password)
    u.save()
    return u

def add_pub(name, placeID):
    p = Pub(name=name, placeID=placeID)
    p.save()
    return p

def add_crawl(creator, name, pubs):
    c = Crawl(id=None, name=name, creator=creator)
    c.save()
    for pub in pubs:
        c.pubs.add(pub)
    c.save()
    return c

def add_review(user, crawl, liked, text):
    r = Review(id=None, user=user, crawl=crawl, liked=liked, text=text)
    r.save()
    return r

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
