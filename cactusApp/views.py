from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from pygrowup import Calculator
from pygrowup import helpers
import datetime

def index(request):
    return render(request, 'cactusApp/index.html')

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
