from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote

from datetime import datetime
import bcrypt

def index(request):
    context = {
        'registered_users' : User.objects.all()
    }
    return render(request, "belt_exam_app/index.html", context)

def register(request):

    #Validation Check
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        plain_text_password = request.POST['password']
        plain_text_conf_password = request.POST['confirmation_password']
        
        #Hash the plaintext password created
        hashed_password = bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

        #If hashed password matches confirmation password, add user to db and move to success page
        if bcrypt.checkpw(plain_text_conf_password.encode(), hashed_password):
        
            #Add user to database if registration successful
            new_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], date_of_birth=request.POST['date_of_birth'], password=hashed_password)
            
            #Set session user_key to id
            request.session['active_user'] = new_user.id
            return redirect('/quotes')
        else:
            return redirect('/')

#Login User: Localhost:8000/login 
def login(request):

    #Validation Check
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if User.objects.filter(email=request.POST['email']):
            user_email = request.POST['email']
            user_password = request.POST['password']

            login_user = User.objects.get(email=user_email)
            login_user_password = request.POST['password']

            passwords_match = bcrypt.checkpw(login_user_password.encode(), login_user.password.encode())
            if passwords_match:
                request.session['active_user'] = login_user.id
                print("Current user updated to: " + str(login_user.name) + str(login_user.alias))
                return redirect('/quotes')
            else:
                print("Invalid credentials")
                return redirect('/')
        else:
            return redirect('/')
    return redirect('/quotes')

#Successful Login/Register: Localhost:8000/quotes
def quotes(request):

    #If an attempt is made to get to dashboard without logging in, redirect to landing page.
    if not 'active_user' in request.session:
        return redirect('/')

    #Mergingn queries. Interested to figure out an alternative way of doing this
    # merged_queries = Trip.objects.filter(Q(created_by=request.session['active_user']) | Q(users_joined=request.session['active_user'])).order_by("-id")

    context = {
        'current_user' : User.objects.get(id=request.session['active_user']),
        'current_date' : datetime.now(),
        'formatted_date': datetime.now().strftime("%Y-%m-%d"),
        'quotable_quotes': Quote.objects.all().exclude(favorited_by=request.session['active_user']),
        # .exclude(favorited_by=request.session['active_user']
        #Exclude current user's quotes from above ^
        'favorite_quotes': Quote.objects.all().filter(favorited_by=request.session['active_user']),

        # 'trip' : Trip.objects.all(),
        # 'merged_queries' : merged_queries,
        # 'trips_excluding_current_user' : Trip.objects.all().exclude(created_by=request.session['active_user']).exclude(users_joined=request.session['active_user']),
        # 'all_trips' : Trip.objects.all(),
    }
    return render(request, "belt_exam_app/quotes.html", context)

#Logout User: Localhost:8000/logout
def logout(request):
    del request.session['active_user']
    return redirect('/')


# Quotes

def add_quote(request):
    print("Adding to quotes")
    content = {
        'quotable_quotes': Quote.objects.all(), #Might not need this
        #Exclude favorites from this list
    }
    # print("created_by: ", Quote.objects.get(created_by=request.session['active_user']))
    print("current user: ", request.session['active_user'])
    print("quoted by: ", request.POST['quoted-by'])
    print("message: ",request.POST['message'])

    errors = Quote.objects.contribute_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:

        Quote.objects.create(content=request.POST['message'], quoted_by=request.POST['quoted-by'], created_by=User.objects.get(id=request.session['active_user']))
        print("quote successfully created")
    
        return redirect('/quotes')

def add_to_favorites(request, id):
    print("Adding quote to favorites")
    Quote.objects.get(id=id).favorited_by.add(User.objects.get(id=request.session['active_user']))
    print("Favorite successfully added")
    return redirect('/quotes')

def remove_from_favorites(request, id):
    print("Removing quote from favorites")
    Quote.objects.get(id=id).favorited_by.remove(User.objects.get(id=request.session['active_user']))
    print("Successfully removed quote from favorites")
    return redirect('/quotes')

def show_user_info(request, id):
    print("Showing user information")
    context = {
        'current_user' : User.objects.get(id=id),
        'posts_by_user' : Quote.objects.all().filter(created_by=User.objects.get(id=id)),
        'num_posts' : Quote.objects.all().filter(created_by=User.objects.get(id=id)).count(),
    }
    return render(request, "belt_exam_app/user_info.html", context)