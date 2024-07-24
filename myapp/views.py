from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist 

def index(request):
    return render(request,'index.html')

#  to validate the the inputs fields , and if there's not any, create a user and save its ID in a session
def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if len(errors) > 0  :
            for error in errors.values(): 
                messages.error(request,error)
            return redirect('/')
        #if there is no errors in inputs, create a user and save it in session
        user = create_user(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, 'Successfully registered.')
        return redirect('success')
    else:
        return render(request,'index.html')
    
# after a successfull  registration or login , render the info of the user in a new page
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = get_id(request.session['user_id'])# call the function in models and save it in a user 

    return render(request,'success.html',{'user':f'{user.firstname} {user.lastname}' })

def login(request):
    if request.method == "POST":
        user = filter_email(request.POST)  # get the the email the user inputted  by using filter crud  from the  filter function in models 
        if user:
            logged_user = user[0]
            # if the password was wrong go to the root page
            if not bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                messages.error(request, 'invalid  passwword or email')
                return redirect('/')
            # if the password was correct go to success page
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                messages.success(request, 'Successfully logged in.')
                return redirect('/success')
        else:
            messages.error(request, "Invalid Inputs") 
    return redirect("/")

# to clear the sessions and go back the root page     
def logout(request):
    request.session.clear()
    return redirect('/')
