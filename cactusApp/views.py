from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Child, Measurement
from django.contrib.auth import login, logout, authenticate
from pygrowup import Calculator
from .getData import draw
from pygrowup import helpers
import datetime
import json


def home(request):
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
        print('////////////')
        print(data)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # return HttpResponseRedirect(reverse("index"))
            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            return JsonResponse({"status": 'ok'})
        else:
            print('#################################')
            return JsonResponse({"message": "Invalid credentials."})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("home"))


def index(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print('////////////')
        print(data)
        childname = data.get('childname')
        childgender = data.get("childgender")
        childdate = data.get("childdate")

        print('/////////////////')
        print(datetime.datetime.now())
        c = datetime.datetime.now()
        z = c.strftime("%Y-%m-%d")
        d1 = datetime.datetime.strptime(z, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(childdate, "%Y-%m-%d")

        age = abs((d2 - d1).days)
        print(round(age/30.4374))
        print(d1.month)
        print(d2.month)

        if (round(age/30.4374)+1) < 24 or (age/30.4374) > 60:
            return JsonResponse({"message": "Child age should be in between 2 and 5 years old."})

        if childgender not in ['boy', 'girl']:
            return JsonResponse({"message": "Child should be a boy or a girl"})

        try:
            child = Child(name=childname, user=request.user, gender=childgender, birthday=childdate)
            child.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message": e})

        return JsonResponse({"status": "ok"})

        # return HttpResponseRedirect(reverse("kids"))

    return render(request, 'cactusApp/home.html')


def kids(request):
    kids = Child.objects.filter(user=request.user)

    context = {
        'kids': kids,
    }

    return render(request, 'cactusApp/child.html', context)


def kid_view(request, kid_id):
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
    # print(list(kid_measure))

    return render(request, 'cactusApp/child_info.html', context)


def measurement(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print('////////////')
        print(data)

        weight = data.get("weight")
        height = data.get("height")
        head_circumference = data.get("head")
        date = data.get("measuredate")
        kid_id = data.get("kid_id")

        kids = Child.objects.get(pk=kid_id)

        bmi = float(weight) / ((float(height) / 100.0))**2

        print(bmi)

        if bmi > 40:
            return JsonResponse({"message": "BMI value is too high."})

        if float(weight) > 40.0:
            return JsonResponse({"message": "Weight value is too high."})

        print(kids.birthday)
        c = kids.birthday
        z = c.strftime("%Y-%m-%d")
        d1 = datetime.datetime.strptime(z, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(date, "%Y-%m-%d")

        age = abs((d2 - d1).days)

        print(d2, d1, age)
        print('////////////////')
        print(age)
        print(bmi)

        measurement = Measurement(weight=weight, height=height,
                                  head_circumference=head_circumference, date=date,
                                  child=kids, age=(round(age/30.4374, 1)), bmi=round(bmi, 2))
        measurement.save()

        return JsonResponse({"status": "ok"})

        # return redirect('charts', kid_id=kid_id)


def chart_weight(request, kid_id):
    child = Child.objects.get(pk=kid_id)
    measurements = Measurement.objects.filter(child=child)
    bmi_list = []
    weight_list = []
    age_list = []
    for measure in measurements:
        bmi_list.append(measure.bmi)
        weight_list.append(measure.weight)
        age_list.append(measure.age)

    if child.gender == 'boy':
        draw('zwtage_m.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)', weight_list, age_list, 'wfa')
        draw('zbmiage_m.csv', "BMI For Age", 'BMI (Kg)', 'Age (Month)', [16], [44], 'bfa')
    else:
        draw('zwtage_f.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)', weight_list, age_list, 'wfa')
        draw('zbmiage_f.csv', "BMI For Age", 'BMI (Kg)', 'Age (Month)', [16], [44], 'bfa')

    return render(request, 'cactusApp/child_chart.html')


def delete_child(request):
    if request.is_ajax() and request.method == "POST":
            if request.user.is_authenticated:
                data = json.loads(request.body)
                id = data.get('id')
                print(id)
                child = Child.objects.get(user=request.user, pk=id)
                child.delete()

    return HttpResponseRedirect(reverse("kids"))



def calculate_score(request):
    '''Index view, render the home page'''
    if request.method == "POST":
        weight = request.POST['weight']
        height = request.POST['height']
        head_circumference = request.POST['HeadCircumference']

        # print("////////////////////")
        # print(weight)
        # print(height)
        # print(head_circumference)
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=False, logger_name='pygrowup',
                       log_level='INFO')

        great_day = datetime.datetime.utcnow().date()
        nine_months_ago = great_day - datetime.timedelta(days=(24 * 30.4374))
        dob = nine_months_ago.strftime("%d%m%y")

        my_child = {'date_of_birth' : dob, 'sex' : 'male', 'weight' : '8.0', 'height' : '69.5'}

        # transform 'male' into 'M'
        valid_gender = helpers.get_good_sex('male')

        # transform something like '100309' into '2009-03-10'
        valid_date = helpers.get_good_date(my_child['date_of_birth'])

        # calculate 9 months from valid_date
        valid_age = helpers.date_to_age_in_months(valid_date[1])

        # calculate weight-for-age zscore
        wfa_zscore_for_my_child = calculator.wfa(my_child['weight'], valid_age, valid_gender)

        # calculate weight-for-age zscore
        bmi = calculator.bmifa(my_child['weight'], valid_age, valid_gender)
        # print(calculator.bmifa.__defaults__)


        print(wfa_zscore_for_my_child, bmi)

    return render(request, 'cactusApp/index.html')
