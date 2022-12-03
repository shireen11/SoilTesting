from dataclasses import fields
from datetime import datetime
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import csv
from soiltesting_app.models import CustomUser,  Staffs,  FeedBackStaffs, TestReport

from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django import forms

def admin_home(request):
   
    staff_count = Staffs.objects.all().count()

    
   
    staff_name_list=[]

    staffs = Staffs.objects.all()
    # for staff in staffs:
       
    #     leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
       
    #     staff_name_list.append(staff.admin.first_name)

   

    context={
    
        "staff_count": staff_count,
   
        "staff_name_list": staff_name_list,
   
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "User Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add User!")
            return redirect('add_staff')



def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "User Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Use.")
            return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "User Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete User.")
        return redirect('manage_staff')






@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)





def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")




# def staff_leave_view(request):
#     leaves = LeaveReportStaff.objects.all()
#     context = {
#         "leaves": leaves
#     }
#     return render(request, 'hod_template/staff_leave_view.html', context)


# def staff_leave_approve(request, leave_id):
#     leave = LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status = 1
#     leave.save()
#     return redirect('staff_leave_view')


# def staff_leave_reject(request, leave_id):
#     leave = LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status = 2
#     leave.save()
#     return redirect('staff_leave_view')



def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')



def staff_profile(request):
    pass


def student_profile(request):
    pass




def add_test(request):
    return render(request, "hod_template/testingreport.html")






def add_test_save(request):
   
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_test')
    else:
    
        x=request.POST.get('staff_id')
        staff_id=Staffs.objects.get(admin=x)
        print(staff_id.id)
        # attendance_date=request.POST.get('attendance_date')
        # attendance_message = request.POST.get('attendance_message')
        # attendance_status = request.POST.get('attendance_status')
        soilmoisture= request.POST.get('soilmoisture')
        ph= request.POST.get('ph')
        metal= request.POST.get('metal')
        # class Meta:
        #     model= AttendanceReportStaff
        #     fields= "__all__"
        #     widgets={
        #         "attendance_date": AdminDateWidget(),
        #         "intime": AdminTimeWidget(),
        #         "outtime": AdminTimeWidget(),
        #     }

        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # address = request.POST.get('address')

        try:
            user = TestReport.objects.create(staff_id=staff_id, soilmoisture=soilmoisture, ph=ph, metal=metal)
            #user.save()
            messages.success(request, "Test Added Successfully!")
            return redirect('add_test')
        except:
            messages.error(request, "Failed to Add Report!")
            return redirect('add_test')

# def staff_attendance_view(request):
#     test = TestReport.objects.all()
#     context = {

#         "test": test
#     }
#     return render(request, 'hod_template/staff_attendance_view.html', context)
######################################################################################################################################################################################################################
def add_test_view(request):
    test = TestReport.objects.all()
    context = {
        "test": test
    }
    return render(request, "hod_template/test_view.html", context)   
########################################################################################################################################
# def export_csv(request):

#     response=HttpResponse(content_type='text/csv')
#     response['Content-Disposition']='attachment; fileName=Attendance'+ '.csv'
#     writer=csv.writer(response)
#     writer.writerow(['Staff ID','Attendance Date','Attendance Date','In Time','Out Time'])


#     attendances = AttendanceReportStaff.objects.all()
#     for attendance in attendances:

#         writer.writerow([attendance.staff_id.id+1, attendance.attendance_date,attendance.intime,attendance.outtime])
#     return response


def reportview(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/reportview.html")

    