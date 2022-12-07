# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from soiltesting_app.EmailBackEnd import EmailBackEnd
import pyrebase



config={
    "apiKey": "AIzaSyCeYvOFOO8MMeyVyqPrCYqCJS95tw0RhlA",
    "authDomain": "test-8b038.firebaseapp.com",
    "databaseURL": "https://test-8b038-default-rtdb.firebaseio.com/",
    "projectId": "test-8b038",
    "storageBucket": "test-8b038.appspot.com",
    "messagingSenderId": "836482545907",
    "appId": "1:836482545907:web:d229ce1c55606ae33b5f86",    
}

firebase= pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()



def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')

            elif user_type == '2':
                
                return redirect('staff_home')

           
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


