from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import pyrebase

from soiltesting_app.models import CustomUser, Staffs, FeedBackStaffs


def staff_home(request):
    # Fetching All Students under Staff


    return render(request, "staff_template/staff_home_template.html")




# def staff_apply_leave(request):
#     # staff_obj = Staffs.objects.get(admin=request.user.id)
#     leave_data = LeaveReportStaff.objects.all()
    
#     context = {
#         "leave_data": leave_data

#     }
#     return render(request, "staff_template/staff_apply_leave_template.html", context)


# def staff_apply_leave_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('staff_apply_leave')
#     else:
#         leave_startdate = request.POST.get('leave_startdate')
#         leave_enddate = request.POST.get('leave_enddate')
#         # leave_message = request.POST.get('leave_message')

#         staff_obj = Staffs.objects.get(admin=request.user.id)
#         try:
#             leave_report = LeaveReportStaff(staff_id=staff_obj, leave_startdate=leave_startdate,leave_enddate=leave_enddate, leave_status=0)
#             leave_report.save()
#             messages.success(request, "Applied for Leave.")
#             return redirect('staff_apply_leave')
#         except:
#             messages.error(request, "Failed to Apply Leave")
#             return redirect('staff_apply_leave')


def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_template/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')




def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')




config={
    "apiKey": "AIzaSyCeYvOFOO8MMeyVyqPrCYqCJS95tw0RhlA",
    "authDomain": "test-8b038.firebaseapp.com",
    "databaseURL": "https://test-8b038-default-rtdb.firebaseio.com/",
    "projectId": "test-8b038",
    "storageBucket": "test-8b038.appspot.com",
    "messagingSenderId": "836482545907",
    "appId": "1:836482545907:web:d229ce1c55606ae33b5f86",
    
    # "apiKey": "AIzaSyB3RdkNPXROHfST-C4qW5yytEFKlJ7j3cQ",
    # "authDomain": "test1-8ae1e.firebaseapp.com",
    # "databaseURL": "https://test1-8ae1e-default-rtdb.asia-southeast1.firebasedatabase.app",
    # "projectId": "test1-8ae1e",
    # "storageBucket": "test1-8ae1e.appspot.com",
    # "messagingSenderId": "824695415456",
    # "appId": "1:824695415456:web:dded808355e6a12d431fc5",
    
}

firebase= pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()


def reportviews(request):
    soilmoisture=database.child('Sensor_Data').child('Soil_Moisture').get().val()
    metaltouch=database.child('Sensor_Data').child('Metal_Touch').get().val()
    # staff = Staffs.objects.get(admin=staff_id)

    
    return render(request, "staff_template/reportview.html",{
        "soilmoisture":soilmoisture,
        "metaltouch":metaltouch
    })


def conclusion_s(request):
    soilmoisture=database.child('Sensor_Data').child('Soil_Moisture').get().val()

    metaltouch=database.child('Sensor_Data').child('Metal_Touch').get().val()

    soilm= (float)(100- ((float)(soilmoisture/1023)*100))

    if soilm>10.00 & soilm<13.00:
        s="Soil is Suitable for construction"
        print(s)
    else:
        s="Not Suitable"
    return render(request, "staff_template/conclusion.html", s)