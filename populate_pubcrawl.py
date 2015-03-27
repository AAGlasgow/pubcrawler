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
    shannon_user = add_user('Shannon', 'shannon@gmail.com', 'myPassword')
    alfred_user = add_user('Alfred', 'alfred@gmail.com', 'myPassword')
    carroll_user = add_user('Carroll', 'carroll@gmail.com', 'myPassword')
    tim_user = add_user('Tim', 'tim@gmail.com', 'myPassword')
    max_user = add_user('Max', 'max@gmail.com', 'myPassword')
    brad_user = add_user('brad', 'shannon@gmail.com', 'myPassword')

    dram_pub = add_pub('DRAM!', 'ChIJKcWC6i1EiEgRrAN2HMyTv0U')
    nice_n_sleazy_pub = add_pub('Nice N Sleazy', 'ChIJ2U7jlChEiEgRaqr1lWpQ2RQ')
    curlers_rest_pub = add_pub('The Curlers Rest', 'ChIJCx0s8c5FiEgR1bZGWa3Jjik')
    guu_pub = add_pub('GUU', 'ChIJLd8s-c1FiEgRCl6u1MNHSNE')
    king_tuts_pub = add_pub('King Tuts Wah Wah Hut', 'ChIJD6VT8idEiEgRu0uJunEd8pc')
    buff_club_pub = add_pub('The Buff Club', 'ChIJRbplOSdEiEgR65ScWqJ11e8')
    bon_accord_pub = add_pub('The Bon Accord', 'ChIJi8Q4pSlEiEgRbkvS7hUgqhY')
    lismore_pub = add_pub('The Lismore', 'ChIJRZDKJttFiEgRkE-fmEHOZdo')
    mcchuills_pub = add_pub('McChuills', 'ChIJeSPzAqRGiEgRfkxFD9ZeqyI')

    johnny_foxes_pub = add_pub('Johnny Foxes', 'ChIJHw24LVJxj0gRlEPBXDd4lns')
    soul_bar_pub = add_pub('Soul Bar', 'ChIJ7VzbOCQOhEgRZHdWb2UyLPc')
    ladywell_tavern_pub = add_pub('Ladywell Tavern','ChIJb0VM9OlchkgRGknIzSfkFAE')
    tron_pub = add_pub('The Tron', 'ChIJ3_xnnYXHh0gR3ihJmEOaSJU')

    get_pished_crawl = add_crawl(butch_user, 'Get Pished', 'In alcohols defense Ive done some dumb shit while completely sober too!', False, "", False, "", [dram_pub, guu_pub, curlers_rest_pub])
    hippy_crawl_crawl = add_crawl(rain_user, 'Hippy Crawl', 'Best chances to come by pills youll have on the toilets', False, "", False, "", [king_tuts_pub, buff_club_pub, nice_n_sleazy_pub])
    clown_crawl = add_crawl(carroll_user, 'Clowns are taking over', "Dead funny you guys need to try that", False, "", True, "Everyone should wear a clown's costume", [dram_pub, nice_n_sleazy_pub, lismore_pub, mcchuills_pub])
    scotland_crawl = add_crawl(max_user, 'Scotland Crawl', 'Have a drink in every bigger city', True, "Always go for the local Whisky", False, "", [mcchuills_pub, johnny_foxes_pub, soul_bar_pub, ladywell_tavern_pub, tron_pub])
    mental_crawl = add_crawl(brad_user, 'Mentally steaming', "There's a bit of walking but a lot of pubs. For you and your best mate!", True, "A pint and shot in each pub", True, "Your right leg must be tied to the left leg of your best mate. No excuses not even for the toilet!", [dram_pub, guu_pub, curlers_rest_pub, bon_accord_pub, nice_n_sleazy_pub, king_tuts_pub, bon_accord_pub, mcchuills_pub])
    edinburgh_crawl = add_crawl(tim_user, 'Edinburgh and back', 'Head over to the eastcoast for a drink and come back to Glasgow.', False, "", False, "", [tron_pub, curlers_rest_pub])
    cookie_crawl = add_crawl(carroll_user, 'Cookie monsters', 'Paint the town red as a cookie monster!', True, "Vodka coke and a cookie", True, "Obviously as a cookie monster", [lismore_pub, buff_club_pub, king_tuts_pub, bon_accord_pub])

    add_review(rain_user, get_pished_crawl, False, 'I didnt like it at all. There was no pub where anyone could sell me some weed or other drugs. Everyone else seemed to enjoy it though. Mainstream shite!')
    add_review(peter_user, get_pished_crawl, True, 'Was fucked that night, woke up the next day in my own sick somewhere in Dundee. Best night evaaa!')
    add_review(peter_user, hippy_crawl_crawl, True, 'Dont like all that drug taking shite. But thumb up cause its dead easy to pull those junky girls haha')
    add_review(butch_user, mental_crawl, True, 'For a good lough for you and your best pal on Saturday night. Just a bit expensive')
    add_review(alfred_user, mental_crawl, True, 'Hilarious')
    add_review(brad_user, get_pished_crawl, True, 'Good pubs and nice student like atmosphere')
    add_review(brad_user, edinburgh_crawl, False, 'Who the fuck would go to Edinburgh for a drink?')
    add_review(shannon_user, scotland_crawl, True, 'Really nice way to see a lot of the country and try the different Whiskys')
    add_review(shannon_user, clown_crawl, True, "Hahahaha it sounds amazing, will try it next weekend")
    add_review(carroll_user, get_pished_crawl, True, 'Easy but good fun')
    add_review(rain_user, cookie_crawl, False, "Do you know the ecological footprint of a single cookie? I don't think that's funny at all")

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
