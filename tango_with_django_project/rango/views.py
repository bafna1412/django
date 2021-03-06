from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_category_list():
    category_list = Category.objects.order_by('-likes')[:5]
    for category in category_list:
        category.url = encode_url(category.name)
    cat_list =  category_list
    return cat_list

@login_required
def restricted(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "Since you're logged in, you can see this text"}
 
    return render_to_response('rango/restricted.html', context_dict, context)

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    cat_list = get_category_list()
    # Query for categories and pages
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Construct a dictionary to pass to the template engine as its context.!
    context_dict = {'categories': category_list, 'pages': page_list, 'cat_list': cat_list}

    # To create the urls for categories
    for category in category_list:
        category.url = encode_url(category.name) 

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    # visits = int(request.COOKIES.get('visits', '0'))

    # Does the cookie last_visit exist?
    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
       # last_visit = request.COOKIES['last_visit']
       # last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if(datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())

            # response.set_cookie('visits', visits + 1)
            # ...and update the last visit cookie, too.
            # response.set_cookie('last_visit', datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

        # Cookie last_visit doesn't exist, so create it to the current date/time.
        # response.set_cookie('last_visit', datetime.now())

    # Return response back to the user, updating any cookies that need changed.
    return render_to_response('rango/index.html', context_dict, context)

def category(request, category_name_url):
    context = RequestContext(request)
    # This replaces underscores in the url with space to get the name.
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list
    context_dict['categories'] = cat_list

    try:
        # Finding the category
        category = Category.objects.get(name = category_name)
        # Retrieving all the pages associated with the category
        pages = Page.objects.filter(category = category)
        # Add the results to the template context under name pages
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_url'] = category_name_url
    except Category.DoesNotExist:
        #Nothing to do here!
        pass

    return render_to_response('rango/category.html', context_dict, context)

def about(request):
    context = RequestContext(request)

    # Note the key boldmessage is the same as {{ boldmessage }} in the template
    # Construct a dictionary to pass to the template engine as its context.!
    context_dict = {'boldmessage': "This is the about page of the tutorial webstie"}

    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict['visits'] = count

    return render_to_response('rango/about.html', context_dict, context)

@login_required
def add_category(request):
    context = RequestContext(request)
    
    # HTTP POST or GET
    if request.method == 'POST':
        form = CategoryForm(request.POST)
       
        # Is the form valid?
        if form.is_valid():
           # Saving the new category
            form.save(commit = True)
           # Return to the Home Page
            return index(request)
        else:
            # Print the errors
            print form.errors

    else:
        # If the request was not a POST, display the form to enter details
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
 
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit = False)
            
            try:
                cat = Category.objects.get(name = category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html', {}, context)

            page.views = 0
            
            page.save()

            return category(request, category_name_url)

        else:
            print name.errors
   
    else:
       form = PageForm()

    return render_to_response('rango/add_page.html', 
                             {'category_name_url': category_name_url, 'category_name': category_name, 'form': form},
                             context)

def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()

    context = RequestContext(request)
    
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered':registered},
            context)

def user_login(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        print user

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is Disabled")
        else:
            print "Invalid Login detalils: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('rango/login.html', context_dict, context)

    else:
        return render_to_response('rango/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    
    return HttpResponseRedirect('/rango/')

def search(request):
    context = RequestContext(request)
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        
        if query:
             # Run our Bing function to get the results list!
             result_list = run_query(query)

    return render_to_response('rango/search.html', {'result_list': result_list}, context)
            
