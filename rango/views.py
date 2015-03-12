from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import UserProfile
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from rango.bing_search import run_query
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import datetime

def index(request):
   
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    

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


    response = render(request,'rango/index.html', context_dict)

    return response

	
def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    return render(request, 'rango/about.html', {'visits': count})

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

    
    return render(request, 'rango/category.html', context_dict)

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

    return render(request, 'rango/add_category.html', {'form': form})

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
    return render(request, 'rango/add_page.html', context_dict)

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

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

    return redirect('/rango/')

@login_required
def register_profile(request):
    current_user = request.user
    try:
        UserProfile.objects.get(user=current_user)
        # This user has already a profile
        return HttpResponseRedirect('/rango/')
    
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
            return HttpResponseRedirect('/rango/')
        else:
            profile_form = UserProfileForm()

        return render(request,
                'rango/profile_registration.html',
                {'profile_form': profile_form} )

@login_required
def profile(request, profile_user_name):
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
    return render(request, 'rango/profile.html', context_dict)

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
            return HttpResponseRedirect('/rango/profile/'+current_user.username+'/')


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
            'rango/edit_profile.html',
            context_dict)


@login_required
def profile_list(request):
    context_dict = {}
    try:  
        users = User.objects.filter()
        context_dict['users'] = users
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/profile_list.html', context_dict)


##def register(request):
##
##    registered = False
##
##    if request.method == 'POST':
##        user_form = UserForm(data=request.POST)
##        profile_form = UserProfileForm(data=request.POST)
##
##        if user_form.is_valid() and profile_form.is_valid():
##            user = user_form.save()
##
##            user.set_password(user.password)
##            user.save()
##
##            profile = profile_form.save(commit=False)
##            profile.user = user
##
##            if 'picture' in request.FILES:
##                profile.picture = request.FILES['picture']
##
##            profile.save()
##
##            registered = True
##
##        else:
##            print user_form.errors, profile_form.errors
##
##    
##    else:
##        user_form = UserForm()
##        profile_form = UserProfileForm()
##
##    return render(request,
##            'rango/register.html',
##            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


##def user_login(request):
##
##    if request.method == 'POST':
##        username = request.POST['username']
##        password = request.POST['password']
##
##
##        user = authenticate(username=username, password=password)
##
##        if user:
##            if user.is_active:
##                login(request, user)
##                return HttpResponseRedirect('/rango/')
##            else:
##                return HttpResponse("Your Rango account is disabled.")
##        else:
##            print "Invalid login details: {0}, {1}".format(username, password)
##            try:
##                User.objects.get(username=username)
##                return HttpResponse("Wrong password supplied.")
##            except:
##                return HttpResponse("Invalid username supplied.")
##
##    else:
##        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

##@login_required
##def user_logout(request):
##    logout(request)
##    return HttpResponseRedirect('/rango/')

    
