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
        if request.user.is_authenticated:
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
        else:
            return JsonResponse({"error": "notAuthorized"})


        # return HttpResponseRedirect(reverse("kids"))

    return render(request, 'cactusApp/home.html')


def kids(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))

    kids = Child.objects.filter(user=request.user)

    context = {
        'kids': kids,
    }

    return render(request, 'cactusApp/child.html', context)


def kid_view(request, kid_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
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
        if request.user.is_authenticated:
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
        else:
            return JsonResponse({"error": "notAuthorized"})

        # return redirect('charts', kid_id=kid_id)


# def chart_weight(request, kid_id):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("home"))
#
#     child = Child.objects.get(pk=kid_id)
#     measurements = Measurement.objects.filter(child=child)
#     bmi_list = []
#     weight_list = []
#     age_list = []
#     for measure in measurements:
#         bmi_list.append(measure.bmi)
#         weight_list.append(measure.weight)
#         age_list.append(measure.age)
#
#     if child.gender == 'boy':
#         draw('zwtage_m.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)', weight_list, age_list, 'wfa')
#         draw('zbmiage_m.csv', "BMI For Age", 'BMI (Kg)', 'Age (Month)', [16], [44], 'bfa')
#     else:
#         draw('zwtage_f.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)', weight_list, age_list, 'wfa')
#         draw('zbmiage_f.csv', "BMI For Age", 'BMI (Kg)', 'Age (Month)', [16], [44], 'bfa')
#
#     return render(request, 'cactusApp/child_chart.html')


def delete_child(request):
    if request.is_ajax() and request.method == "POST":
            if request.user.is_authenticated:
                data = json.loads(request.body)
                id = data.get('id')
                print(id)
                child = Child.objects.get(user=request.user, pk=id)
                child.delete()

    return HttpResponseRedirect(reverse("kids"))



# def chart_js(request, kid_id):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("home"))
#
#     child = Child.objects.get(pk=kid_id)
#     measurements = Measurement.objects.filter(child=child)
#     bmi_list = []
#     weight_list = []
#     age_list = []
#     for measure in measurements:
#         bmi_list.append(measure.bmi)
#         weight_list.append(measure.weight)
#         age_list.append(measure.age)
#
#     age, p1, p2, p3, p4, p5, p6, p7, p8 = getData('zwtage_m.csv')
#     print('?????????????????????????')
#     res = dict(zip(age, p1))
#     print(res)
#     # print(p8)
#     context = {
#         'age': age,
#         'p1': p1,
#         'p2': p2,
#         'p3':p3,
#         'p4':p4,
#         'p5':p5,
#         'p6':p6,
#         'p7':p7,
#         'p8':p8,
#     }
#     return render(request, 'cactusApp/chart_js.html', context)

def chart_weight(request, kid_id):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("home"))
    #
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
        weight = getData('zwtage_m.csv')
        bmi = getData('zbmiage_m.csv')
    else:
        weight = getData('zwtage_f.csv')
        bmi = getData('zbmiage_f.csv')

    # test = [{'x': 32, 'y': 20}]
    agee = [29, 32, 40]
    we = [18, 20, 12]

    print("????????????????")
    print(age_list)
    print(weight_list)
    print(bmi_list)
    context = {
        'weight': weight,
        'bmi': bmi,
        'age': age_list,
        "weight_values": weight_list,
        'bmi_values': bmi_list,
    }
    return render(request, 'cactusApp/chart_js.html', context)

    # return render(request, 'cactusApp/child_chart.html')
