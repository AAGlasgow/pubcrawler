import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from pubcrawl.models import Category, Page, Crawl, Pub, Review, Crawl_Pub
from django.contrib.auth.models import User


def populate():

    butch_user = add_user('Butch', 'butch@gmail.com', 'myPassword')
    peter_user = add_user('Peter', 'peter@gmail.com', 'myPassword')
    rain_user = add_user('Rain', 'rain@gmail.com', 'myPassword')
    test_user = add_user('test', 'test@gmail.com', 'test')

    dram_pub = add_pub('DRAM!', 'ChIJKcWC6i1EiEgRrAN2HMyTv0U')
    nice_n_sleazy_pub = add_pub('Nice N Sleazy', 'ChIJ2U7jlChEiEgRaqr1lWpQ2RQ')
    curlers_rest_pub = add_pub('The Curlers Rest', 'ChIJCx0s8c5FiEgR1bZGWa3Jjik')
    guu_pub = add_pub('GUU', 'ChIJLd8s-c1FiEgRCl6u1MNHSNE')
    king_tuts_pub = add_pub('King Tuts Wah Wah Hut', 'ChIJD6VT8idEiEgRu0uJunEd8pc')
    buff_club_pub = add_pub('The Buff Club', 'ChIJRbplOSdEiEgR65ScWqJ11e8')

    get_pished_crawl = add_crawl(butch_user, 'Get Pished', 'In alcohols defense Ive done some dumb shit while completely sober too!', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])
    hippy_crawl_crawl = add_crawl(rain_user, 'Hippy Crawl', 'Best chances to come by pills youll have on the toilets', False, "", False, "", [king_tuts_pub, buff_club_pub, nice_n_sleazy_pub])
    test_generic_1 = add_crawl(butch_user, 'test_1', '...', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])
    test_generic_2 = add_crawl(butch_user, 'test_2', '...', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])
    test_generic_3 = add_crawl(butch_user, 'test_3', '...', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])
    test_generic_4 = add_crawl(butch_user, 'test_4', '...', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])
    test_generic_5 = add_crawl(butch_user, 'test_5', '...', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])

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
    print ""
    print "Crawl_Pub:"
    for p in Crawl_Pub.objects.all():
        print p


def add_user(name, email, password):
    u = User(username=name, email=email, password=password)
    u.save()
    return u

def add_pub(name, placeID):
    p = Pub(name=name, placeID=placeID)
    p.save()
    return p

def add_crawl(creator, name, description, drink, drinkDescription, costume, costumeDescription, pubs):
    c = Crawl(id=None, name=name, creator=creator, description=description, drink=drink, drinkDescription=drinkDescription, costume=costume, costumeDescription=costumeDescription)
    c.save()
    for pub in pubs:
        c.add_pub(pub)
    c.save()
    return c

def add_review(user, crawl, liked, text):
    r = Review(id=None, user=user, crawl=crawl, liked=liked, text=text)
    if(liked):
        c = Crawl.objects.get(slug=crawl.slug)
        score = c.score+1
        c.score = score
        c.save()
    r.save()
    return r

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
