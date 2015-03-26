from django.shortcuts import render, redirect
from django.http import HttpResponse
from pubcrawl.models import Crawl, Review, UserProfile, Crawl_Pub
from pubcrawl.forms import UserForm, UserProfileForm, ReviewForm, CrawlForm
from pubcrawl.bing_search import run_query
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q

def index(request):

    crawl_list = Crawl.objects.order_by('name')
    context_dict = {'crawls': crawl_list}

    review_list = Review.objects.order_by('crawl')
    context_dict['reviews'] = review_list

    crawl_pub_list = Crawl_Pub.objects.order_by('position')
    context_dict['crawl_pub'] = crawl_pub_list
    

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'pubcrawl/index.html', context_dict)

    return response

    
def welcome(request):
    return render(request, 'pubcrawl/welcome.html')

def category(request, category_name_slug):

    
    context_dict = {}

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            context_dict['result_list'] = run_query(query)

    try:
        
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        
        pages = Page.objects.filter(category=category)

        
        context_dict['pages'] = pages
        
        context_dict['category'] = category
    except Category.DoesNotExist:
        
        pass

    
    return render(request, 'pubcrawl/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors

    else:
        form = CategoryForm()

    return render(request, 'pubcrawl/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
            
    else:
        form = PageForm()

    context_dict = {'form':form, 'category':cat, 'failedURL':category_name_slug}
    return render(request, 'pubcrawl/add_page.html', context_dict)

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request, 'pubcrawl/search.html', {'result_list': result_list})

def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(title=page_id)
                page.views = page.views+1
                #The associated category needs to be updated as well
                cat = Category.objects.get(name=page.category)
                cat.views = cat.views + 1
                cat.save()
                page.save()
                return redirect(page.url)
            except:
                print "Page does not exists"

    return redirect('/pubcrawl/')

@login_required
def register_profile(request):
    current_user = request.user
    try:
        UserProfile.objects.get(user=current_user)
        # This user has already a profile
        return HttpResponseRedirect('/pubcrawl/')
    
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            profile_form = UserProfileForm(data=request.POST)

            if profile_form.is_valid():

                profile = profile_form.save(commit=False)
                profile.user = current_user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                profile.save()
            else:
                print profile_form.errors
            return HttpResponseRedirect('/pubcrawl/')
        else:
            profile_form = UserProfileForm()

        return render(request,
                'pubcrawl/profile_registration.html',
                {'profile_form': profile_form} )

@login_required
def profile(request, profile_user_name, pageContent):
    print pageContent

    context_dict = {}

    if pageContent == 'crawl':
        contentCrawl = True
    else:
        contentCrawl = False

    context_dict['contentCrawl'] = contentCrawl

    try:
        user = User.objects.get(username=profile_user_name)
        context_dict['requested_user'] = user
        if contentCrawl == True:
            crawls = Crawl.objects.filter(creator=user)
        else:
            reviews = Review.objects.filter(user=user)
            crawls = []
            for r in reviews:
                crawls.append(r.crawl)
            context_dict['reviews'] = reviews
        context_dict['crawls'] = crawls
        context_dict['crawl_pub'] = Crawl_Pub.objects.order_by('crawl')
    except Category.DoesNotExist:
        pass
    return render(request, 'pubcrawl/profile.html', context_dict)

@login_required
def account_details(request, profile_user_name):
    context_dict = {}
    try:
        user = User.objects.get(username=profile_user_name)
        context_dict['requested_user'] = user
        try:
            profile = UserProfile.objects.get(user=user)
            context_dict['profile_exists'] = True
            context_dict['profile'] = profile
        except UserProfile.DoesNotExist:
            context_dict['profile_exists'] = False
    except Category.DoesNotExist:
        pass
    return render(request, 'pubcrawl/account_details.html', context_dict)

@login_required
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        field = user_form.fields['email']
        data = field.widget.value_from_datadict(user_form.data, user_form.files, user_form.add_prefix('email'))
        try:
            current_user.email = field.clean(data)
            valid_update = True
        except:
            valid_update = False
        current_user.save(update_fields=['email'])

        try:
            profile = UserProfile.objects.get(user=current_user)
            # This user has already a profile
            field = profile_form.fields['website']
            data = field.widget.value_from_datadict(profile_form.data, profile_form.files, profile_form.add_prefix('website'))
            try:
                profile.website = field.clean(data)
            except:
                valid_update = False
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            
    
        except UserProfile.DoesNotExist:
            profile_form = UserProfileForm(data=request.POST)

            if profile_form.is_valid():

                profile = profile_form.save(commit=False)
                profile.user = current_user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                profile.save()
            else:
                print profile_form.errors
                valid_update = False

        if valid_update:
            return HttpResponseRedirect('/pubcrawl/profile/'+current_user.username+'/')


    context_dict = {}
    user_form = UserForm(initial={'email': current_user.email})
    try:
        profile = UserProfile.objects.get(user=current_user)
        context_dict['profile_exists'] = True
        context_dict['profile'] = profile
        profile_form = UserProfileForm(initial={'website': profile.website})
    except UserProfile.DoesNotExist:
        context_dict['profile_exists'] = False
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form

    return render(request,
            'pubcrawl/edit_profile.html',
            context_dict)


@login_required
def profile_list(request):
    context_dict = {}
    try:  
        users = User.objects.filter()
        context_dict['users'] = users
    except Category.DoesNotExist:
        pass
    return render(request, 'pubcrawl/profile_list.html', context_dict)


def create_pubcrawl(request):
    form = CrawlForm()
    return render(request, 'pubcrawl/create_pubcrawl.html', {'form' : form})


@login_required
def restricted(request):
    return render(request, 'pubcrawl/restricted.html')


@login_required
def rate_crawl(request):

    crawl_id = None
    if request.method == 'GET':
        #crawl_id & crawl_rating are passed in via Ajax in HTTP.
        crawl_id = request.GET['crawl_id']

    score = 0
    if crawl_id:
        crawl = Crawl.objects.get(slug = crawl_id)
        if crawl:
            score = crawl.score + 1
            crawl.score = score
            crawl.save()
            
            user = request.user
            try:
                review = Review.objects.get(user = user, crawl = crawl)
                if review.liked == True:
                    review.liked = False
                    score = crawl.score - 2
                    crawl.score = score
                    crawl.save()
                else:
                    review.liked = True
                review.save()
            except:
                review = Review.objects.create(user = user, crawl = crawl, liked = True)
                review.save()

    return HttpResponse(score)


def crawl(request, crawl_name):
    context_dict = {}

    try:
        crawl = Crawl.objects.get(slug=crawl_name)
        context_dict['crawl_name'] = crawl.name
        context_dict['crawl'] = crawl
        context_dict['crawl_pub'] = Crawl_Pub.objects.order_by('position')
        crawl_pub = Crawl_Pub.objects.order_by('position')

        pubs = []
        for pub in crawl_pub.all():
            if pub.crawl == crawl:
                pubs.append(pub.pub.placeID)
        context_dict['start'] = pubs[0]
        context_dict['end'] = pubs[-1]
        context_dict['waypoints'] = pubs
        context_dict['reviews'] = Review.objects.filter(crawl=crawl).order_by('-dateTime')
        reload = False
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                # Save the new category to the database.
                # Now call the index() view.
                # The user will be shown the homepage.
                field = form.fields['text']
                data = field.widget.value_from_datadict(form.data, form.files, form.add_prefix('text'))
                try:
                    review = Review.objects.get(user = request.user, crawl = crawl)
                    review.text = field.clean(data)
                    review.save()
                except:
                    review = Review.objects.create(user = request.user, crawl = crawl, liked = False, text=field.clean(data))
                    review.save()
            else:
                # The supplied form contained errors - just print them to the terminal.
                reload = True
        else:
            reload = True
        try:
            user_review = Review.objects.get(crawl=crawl, user=request.user)
            context_dict['user_review'] = user_review
            form = ReviewForm(initial={'text': user_review.text})
        except:
            form = ReviewForm()
    except Crawl.DoesNotExist:
        pass

    if reload:
        context_dict['form'] = form
    else:
        context_dict['form'] = None

    return render(request, 'pubcrawl/crawl.html', context_dict)

def get_crawl_list(crawls, sort_by='name', start_at=0):
    crawl_list = []
    if sort_by == 'name':
        if crawls != None:
            crawl_list = Crawl.objects.filter(slug__in=crawls).order_by('name')[start_at:start_at+3]
        else:
            crawl_list = Crawl.objects.order_by('name')[start_at:]
    elif sort_by == 'score':
        if crawls != None:
            crawl_list = Crawl.objects.filter(slug__in=crawls).order_by('-score')[start_at:start_at+3]
        else:
            crawl_list = Crawl.objects.order_by('-score')[start_at:start_at+3]
    
    return crawl_list

def crawl_list(request):
    context_dict = {}

    crawl_pub_list = Crawl_Pub.objects.order_by('position')
    context_dict['crawl_pub'] = crawl_pub_list

    sort_by = "name"
    start_at = 0
    if request.method == "GET":
        sort_by = request.GET.get('sort_by')
        crawls = request.GET.getlist('crawls[]')
        start_at = int(request.GET.get('start_at'))
    else:
        crawls = None

    context_dict['crawls'] = get_crawl_list(crawls, sort_by, start_at)
    
    return render(request, 'pubcrawl/crawl_list.html', context_dict)

def results(request,search_tag=""):
    result = []
    context_dict = []
    if request.method == 'POST':
        search = request.POST['s']
    else:
        search = search_tag
    result = get_results(request, search) # Delivers a list of found stuff

    context_dict = {'crawls': result}

    review_list = Review.objects.order_by('crawl')
    context_dict['reviews'] = review_list

    crawl_pub_list = Crawl_Pub.objects.order_by('position')
    context_dict['crawl_pub'] = crawl_pub_list

    context_dict['search_tag'] = search

    return render(request, 'pubcrawl/index.html', context_dict)


def get_results(request, query):
    results = []
    # Split the string to the list without spaces and commas
    for crawl in Crawl.objects.filter(name__contains=query):
        results.append(crawl)

    for crawl_pub in Crawl_Pub.objects.filter(Q(pub__name__contains=query) | Q(pub__slug__contains=query)):
        results.append(crawl_pub.crawl)

    return results

        
    
    
    