from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Query for categories and pages
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Construct a dictionary to pass to the template engine as its context.!
    context_dict = {'categories': category_list, 'pages': page_list}

    # To create the urls for categories
    for category in category_list:
        category.url =encode_url(category.name) 

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dict, context)

def category(request, category_name_url):
    context = RequestContext(request)
    # This replaces underscores in the url with space to get the name.
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name}
    
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

    return render_to_response('rango/about.html', context_dict, context)

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



