from django.test import TestCase
from pubcrawl.models import Pub, Crawl, Review
from django.contrib.auth.models import User

class CrawlTestCase(TestCase):
    string = 'Awesome crawl, you should try it'
    def setUp(self):
        user = User.objects.create(username='Butch', email='butch@gmail.com', password='myPassword')
        self.crawl = Crawl.objects.create(creator=user, name='Get Pished', description=self.string)

    def test_crawl_has_name(self):
        self.assertEqual(self.crawl.name, 'Get Pished')

    def test_crawl_has_right_user(self):
        self.assertEqual(self.crawl.creator.username, 'Butch')

    def test_crawl_has_right_description(self):
        self.assertEqual(self.crawl.description, self.string)

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


# Create your tests here.
