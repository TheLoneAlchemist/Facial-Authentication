from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .models import User

import os
import base64
from pathlib import Path

from .ImageAuth import FindMatch, ImageAuthentication


def base64Toimage(encodedString, name):
    decoded_data = base64.b64decode(encodedString)
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        # print(f'{BASE_DIR}\media\\faces\{name}.jpeg')
        # filepath = f'{BASE_DIR}\media\\faces\{name}.jpeg'

        # with open(filepath, 'wb') as f:

        #     f.write(decoded_data)
        #     f.close()
        #     return filepath
        from PIL import Image
        import io
        filepath = f"media/faces/{name}.png"
        img = Image.open(io.BytesIO(decoded_data))
        path = img.save(filepath,'png')
        return f"faces/{name}.png"
    except Exception as e:
        print(e)
        print("Path Error!...........")
        return None


def index(request):
    if request.method == "POST":
        print(request.POST)
        return JsonResponse({"message": "Request handdled.."})
        
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        image64 = request.POST['image64']

        userobj = User.objects.filter(email__exact=email).first()
        if userobj is not None:
            msg = "Email already Exist!..."
            return HttpResponse(msg)
        if image64 == "":
            msg = "Please Send Image Data..."
            return HttpResponse(msg)
        if password1 != password2:
            msg = "Both password should be same..."
            return HttpResponse(msg)

        try:
            decodedImage = base64Toimage(image64[21:], email)
            if decodedImage is not None:

                imagequeryset = User.objects.values_list('image', flat=True)
                match = FindMatch(decodedImage, list(imagequeryset))
                if match == True:
                    msg = "Face is Already Registed..."
                    return HttpResponse(msg)
                else:

                    user = User.objects.create_user(first_name=fname, last_name=lname,
                                                    email=email, password=password1, image=decodedImage)
                    user.save()
                    messages.success(
                        request, f"Hii! {fname}, Welcome to Acts of Kindness!")
                    return HttpResponse('signup')
            else:
                msg = "Image decoding Error!...."
                return HttpResponse(msg)
        except IndexError:
            msg = "Face not Found!...Kindly Properly Face towards Camera"
            return HttpResponse(msg)

    return render(request, 'signup.html')


def Login(request):
    # if request.user.is_authenticated:
    #     msg = "You are already logged in!... Kindly logout before sign in to anther account..."
    #     return HttpResponseBadRequest(msg)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        image64 = request.POST['image64']
        msg = ''
        if image64 == "":
            msg = "Please Send Image Data..."
            return HttpResponse(msg)

        try:
            decodedImage = base64Toimage(image64[21:], f'{email}[RI]')
            if decodedImage is not None:

                userobj = User.objects.filter(email__exact=email).first()
                if userobj is None:
                    return HttpResponse("Email Does't Exist")
                # userobj = User.objects.get(email__exact=email)
                user = authenticate(email=email, password=password)
                image1 = userobj.image
                imgauth = ImageAuthentication(image1, decodedImage)
                print("-------------------------------------------------")
                print(imgauth[0], user)
                try:
                    if user is None:
                        msg = "Invalid Password!"
                        return HttpResponse(msg)
                    if imgauth[0] == False:
                        msg = "Image Couldn't match..."
                        print(msg)
                        return HttpResponse(msg)

                    elif (imgauth[0] == True) & (user is not None):
                        login(request, user)
                        messages.success(
                            request, f"Welcome {request.user}.Glad to have you back!")
                        return HttpResponse('login')
                    else:
                        msg = "Invalid Credential! Kindly put right "
                        return HttpResponse(msg)
                except ValueError:
                    msg = "Image authentication failed!"
                    return HttpResponse(msg)
            else:
                msg = "Image Error!...."
        except IndexError:
            msg = "Kindly Properly Face to the Camera!..."
            print(msg)
            return HttpResponse(msg)
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('/login')

def About(request):
    return render(request,'about.html')


def Profile(request):
    if request.user.is_anonymous:
        messages.warning(request,"You need to login first...")
        return redirect('/login')
    else:
        userobj = User.objects.get(email = request.user.email)
        print(userobj.image)
    return render(request,'profile.html',{'userobj' : userobj})

def DeleteProfile(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    userobj = User.objects.get(email__exact = request.user.email) 
    print(userobj.image)
    print(f'{BASE_DIR}/media/face/{userobj.image}')
    if request.user.is_anonymous:
        messages.error(request,"Cann't Delete User... You have login first!")
        return redirect('login')
    else:
        if request.method == 'POST':
            userobj = User.objects.get(email__exact = request.user.email)
            logout(request)
            userobj.delete()

            messages.success(request,f"{userobj.first_name} has been deleted!. Hope you back soon...")
            return redirect('/')
    return HttpResponseNotAllowed('You are going through wrong way!')


def Contact(request):
    return render(request,'contact.html')