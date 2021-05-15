from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Child, Measurement
from django.contrib.auth import login, logout, authenticate
from .getData import draw, getData
import datetime
import json


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return render(request, 'cactusApp/index.html')


def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password')

        if not password == password2:
            return JsonResponse({"message": "Passwords don't match."})

        try:
            user = User.objects.create_user(username=username, password=password)
            user.username = username
            user.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Username already exists!"})

        login(request, user)
        return JsonResponse({"status": 'ok'})


def Login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": 'ok'})
        else:
            return JsonResponse({"message": "Invalid credentials."})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("home"))


def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            # Get the child data
            childname = data.get('childname')
            childgender = data.get("childgender")
            childdate = data.get("childdate")
            # Validate the child's age to be in between 2 and 5 years old
            c = datetime.datetime.now()
            z = c.strftime("%Y-%m-%d")
            d1 = datetime.datetime.strptime(z, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(childdate, "%Y-%m-%d")
            age = abs((d2 - d1).days)

            if (round(age/30.4374)+1) < 24 or (age/30.4374) > 60:
                return JsonResponse({"message": "Child age should be in between 2 and 5 years old."})

            if childgender not in ['boy', 'girl']:
                return JsonResponse({"message": "Child should be a boy or a girl"})
            # Add the child to DB
            try:
                child = Child(name=childname, user=request.user, gender=childgender, birthday=childdate)
                child.save()
            except Exception as e:
                print(e)
                return JsonResponse({"message": e})

            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"error": "notAuthorized"})


        # return HttpResponseRedirect(reverse("kids"))

    return render(request, 'cactusApp/home.html')


def kids(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    # Get the list of children
    kids = Child.objects.filter(user=request.user)

    context = {
        'kids': kids,
    }

    return render(request, 'cactusApp/child.html', context)


def kid_view(request, kid_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    # Get the page about child information
    kids = Child.objects.get(pk=kid_id)
    kid_measure = Measurement.objects.filter(child=kids)
    measure_found = 0
    if kid_measure:
        measure_found = 1


    context = {
        'kid_id': kid_id,
        'measure_found': measure_found,
        'measurements': kid_measure,
    }

    return render(request, 'cactusApp/child_info.html', context)


def measurement(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Get the child's measurement
            data = json.loads(request.body)
            weight = data.get("weight")
            height = data.get("height")
            head_circumference = data.get("head")
            date = data.get("measuredate")
            kid_id = data.get("kid_id")

            kids = Child.objects.get(pk=kid_id)
            # calculate the BMI
            bmi = float(weight) / ((float(height) / 100.0))**2
            # Validate the BMI and weight values to be logic
            if bmi > 40:
                return JsonResponse({"message": "BMI value is too high."})

            if float(weight) > 40.0:
                return JsonResponse({"message": "Weight value is too high."})

            c = kids.birthday
            z = c.strftime("%Y-%m-%d")
            d1 = datetime.datetime.strptime(z, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(date, "%Y-%m-%d")

            age = abs((d2 - d1).days)
            # Added a measurement to DB
            measurement = Measurement(weight=weight, height=height,
                                      head_circumference=head_circumference, date=date,
                                      child=kids, age=(round(age/30.4374, 1)), bmi=round(bmi, 2))
            measurement.save()

            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"error": "notAuthorized"})


def delete_child(request):
    if request.is_ajax() and request.method == "POST":
            if request.user.is_authenticated:
                data = json.loads(request.body)
                id = data.get('id')
                child = Child.objects.get(user=request.user, pk=id)
                child.delete()
                return JsonResponse({"status": "ok"})

    return HttpResponseRedirect(reverse("kids"))


def chart_weight(request, kid_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    # Get the child measurement from DB
    child = Child.objects.get(pk=kid_id)
    measurements = Measurement.objects.filter(child=child)
    # Get a list of bmi, weight and age for the child
    bmi_list = []
    weight_list = []
    age_list = []
    for measure in measurements:
        bmi_list.append(measure.bmi)
        weight_list.append(measure.weight)
        age_list.append(measure.age)

    # Open and Read the csv file to get the data from it(weight/bmi values for each age)
    if child.gender == 'boy':
        weight = getData('zwtage_m.csv')
        bmi = getData('zbmiage_m.csv')
    else:
        weight = getData('zwtage_f.csv')
        bmi = getData('zbmiage_f.csv')

    context = {
        'weight': weight,
        'bmi': bmi,
        'age': age_list,
        "weight_values": weight_list,
        'bmi_values': bmi_list,
    }
    return render(request, 'cactusApp/chart_js.html', context)
