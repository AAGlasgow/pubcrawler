from django.test import TestCase
from pubcrawl.models import Pub, Crawl, Review
from django.contrib.auth.models import User
import datetime


class CrawlTestCase(TestCase):
    string = 'Awesome crawl, you should try it'
    drinkDescr = 'A Cider in every pub'
    costumeDescr = 'Nobody would see this if costume==False'
    def setUp(self):
        user = User.objects.create(username='Butch', email='butch@gmail.com', password='myPassword')
        self.dram_pub = Pub.objects.create(name='DRAM!', placeID='ChIJKcWC6i1EiEgRrAN2HMyTv0U')
        self.nice_n_sleazy_pub = Pub.objects.create(name='Nice N Sleazy', placeID='ChIJ2U7jlChEiEgRaqr1lWpQ2RQ')
        self.crawl = Crawl.objects.create(creator=user, name='Get Pished', description=self.string)
        self.mydatetime = datetime.datetime.now() #implemented here to keep mydate as close as possible to the crawl object
        self.crawl.pubs.add(self.dram_pub)
        self.crawl.pubs.add(self.nice_n_sleazy_pub)
        self.crawl.drink=True
        self.crawl.drinkDescription=self.drinkDescr
        self.crawl.costume=False
        self.crawl.costumeDescription=self.costumeDescr
        self.crawl.save()

    def test_date_time(self):
        self.assertEqual(self.mydatetime.year, self.crawl.dateTime.year)
        self.assertEqual(self.mydatetime.month, self.crawl.dateTime.month)
        self.assertEqual(self.mydatetime.day, self.crawl.dateTime.day)
        self.assertEqual(self.mydatetime.hour, self.crawl.dateTime.hour)
        self.assertEqual(self.mydatetime.minute, self.crawl.dateTime.minute)
        self.assertEqual(self.mydatetime.second, self.crawl.dateTime.second)

    def test_crawl_has_right_name(self):
        self.assertEqual(self.crawl.name, 'Get Pished')

    def test_crawl_has_right_user(self):
        self.assertEqual(self.crawl.creator.username, 'Butch')

    def test_crawl_has_right_description(self):
        self.assertEqual(self.crawl.description, self.string)

    def test_crawl_has_right_pubs(self):
        self.assertIn(self.nice_n_sleazy_pub, self.crawl.pubs.all())
        self.assertIn(self.dram_pub, self.crawl.pubs.all())

    def test_crawl_has_right_drink(self):
        self.assertEqual(self.crawl.drink, True)
        self.assertEqual(self.crawl.drinkDescription, self.drinkDescr)

    def test_crawl_has_right_costume(self):
        self.assertEqual(self.crawl.costume, False)
        self.assertEqual(self.crawl.costumeDescription, self.costumeDescr)

class ReviewTestCase(TestCase):
    string = 'Awesome crawl, you should try it'
    def setUp(self):
        user = User.objects.create(username='Rain', email='rain@gmail.com', password='myPassword')
        user2= User.objects.create(username='Butch', email='butch@gmail.com', password='myPassword')
        crawl = Crawl.objects.create(creator=user, name='Make Love No War', description='My favourite')
        self.review = Review.objects.create(user=user2, crawl=crawl, liked=True, text=self.string)

    def test_review_text(self):
        self.assertEqual(self.review.text, self.string)

    def test_crawl_creator(self):
        self.assertEqual(self.review.crawl.creator.username, 'Rain')

    def test_crawl_name(self):
        self.assertEqual(self.review.crawl.name, 'Make Love No War')

    def test_liked(self):
        self.assertEqual(self.review.liked, True)

class PubTestCase(TestCase):
    stringName = 'DRAM!'
    stringPlaceID='ChIJKcWC6i1EiEgRrAN2HMyTv0U'
    def setUp(self):
         self.pub = Pub.objects.create(name=self.stringName, placeID=self.stringPlaceID)

    def test_pub_name(self):
        self.assertEqual(self.pub.name, self.stringName)

    def test_pub_ID(self):
        self.assertEqual(self.pub.placeID, self.stringPlaceID)


# Create your tests here.
