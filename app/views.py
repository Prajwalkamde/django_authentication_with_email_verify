from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_login(request):
    # if request.user_obj.is_authenticated:
    #     return redirect("/")

    if request.method == 'POST':
        username = request.POST.get('loginusername')
        password = request.POST.get('loginpass')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.warning(request,"No user found!")
            return redirect('login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_email_verified:
            messages.warning(request,"Your account is not verified. please check your mail.")
            return redirect('login')

        user_obj = authenticate(username=username,password=password)

        # else:
        #     try:
        #         user_obj = authenticate(username=User.objects.get(email=username),password=password)
        #     except:
        #         user_obj = authenticate(username=username,password=password)
         

        if user_obj is not None:
            login(request,user_obj)
            messages.success(request,"You have successfully logged in !")
            return redirect('/')

        else:
            messages.warning(request,"Invalid Credentials! Please enter correct username or password !")
            return redirect('login')

    return render(request, 'login.html')




def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        

        if User.objects.filter(username=username).first():
            messages.warning(request,"Username is already taken")
            return HttpResponseRedirect(request.path_info)

        if User.objects.filter(email=email).first():
            messages.warning(request,"Email is already taken")
            return HttpResponseRedirect(request.path_info)

        if pass1 != pass2:
            messages.warning(request,"Both passwords should match!")
            return HttpResponseRedirect(request.path_info)


        user_obj = User.objects.create_user(username=username, email=email, password=pass1)
        user_obj.save()
        email_token = str(uuid.uuid4())

        profile_obj = Profile.objects.create(user=user_obj, email_token=email_token)
        profile_obj.save()
        send_mail_after_signup(email, email_token)
        messages.success(request,"Email has been sent to verify your account!")
        return redirect('signup')


    return render(request, 'signup.html')





# for verifying email
def send_mail_after_signup( email, email_token):
    subject = "Action Needed!!! Your account needs to be verify!"
    # message = f"Please click on the link to verify your account. http://127.0.0.1:8000/verify/{email_token}"
    message = f"Please click on the link to verify your account. https://django-auth.up.railway.app/verify/{email_token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



# for sending forget password link
def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    # message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
    message = f'Hi , click on the link to reset your password https://django-auth.up.railway.app/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



def user_verify(request, email_token):
    try:
        profile_obj = Profile.objects.filter(email_token=email_token).first()

        if profile_obj:
            if profile_obj.is_email_verified:
                messages.info(request,"Your account is already verified.")
                print(messages)
                return redirect('login')


            profile_obj.is_email_verified = True
            profile_obj.save()
            messages.success(request,"Your account has been verified. Now you can login.")
            return redirect('login')

        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return render(request, 'login.html')
    # return render(request, 'verify.html')





def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.warning(request, 'No user id found.')
                return redirect(f'/change_password/{token}/')
                
            
            if  new_password != confirm_new_password:
                messages.warning(request, 'Both passwords should  be equal!')
                return redirect(f'/change_password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request,"Your password has been changed. login with new password")
            return redirect('login')
            
            
            
        
        
    except Exception as e:
        print(e)
    return render(request , 'change_password.html' , context)


import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            loginusername = request.POST.get('loginusername')
            
            if not User.objects.filter(username=loginusername).first():
                messages.warning(request, 'Not user found with this username.')
                return redirect('/forget_password/')
            
            user_obj = User.objects.get(username = loginusername)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent to reset your password.')
            return redirect('/forget_password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forget_password.html')






# @login_required(login_url='/login')
def user_profile(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        return render(request,'profile.html')


def user_logout(request):
    logout(request)
    messages.success(request,"You have been logged out !")
    return redirect('login')
    

