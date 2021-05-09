import csv
import matplotlib.pyplot as plt
import numpy as np
import os


def getData(file_path):
    age = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    p6 = []
    p7 = []
    p8 = []
    workpath = os.path.dirname(os.path.abspath(__file__))
    # os.path.join(workpath, 'file.csv'), 'rb')
    with open(os.path.join(workpath, 'data/'+f'{file_path}')) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            age.append(float(row['Agemos']))
            p1.append(float(row['-1.5']))
            p2.append(float(row['-1']))
            p3.append(float(row['-0.5']))
            p4.append(float(row['0']))
            p5.append(float(row['0.5']))
            p6.append(float(row['1']))
            p7.append(float(row['1.5']))
            p8.append(float(row['2']))


    return age, p1, p2, p3, p4, p5, p6, p7, p8


def draw(data, title, y_lable, x_lable, child_value, child_age, img_name):
    workpath = os.path.dirname(os.path.abspath(__file__))
    age, p1, p2, p3, p4, p5, p6, p7, p8 = getData(data)
    plt.plot(age, p1, label='p1')
    plt.plot(age, p2, label='p2')
    plt.plot(age, p3, label='p3')
    plt.plot(age, p4, label='p4')
    plt.plot(age, p5, label='p5')
    plt.plot(age, p6, label='p6')
    plt.plot(age, p7, label='p7')
    plt.plot(age, p8, label='p8')

    plt.plot(child_age, child_value, marker='o', ms=10, mec='r', label='Child')
    plt.title(title)
    plt.ylabel(y_lable)
    plt.xlabel(x_lable)

    plt.legend()

    x_ticks = np.arange(24, 60, 2)
    # x_ticks = np.arange(24, 240, 20)
    plt.xticks(x_ticks)

    y_ticks = np.arange(5, 50, 2)
    plt.yticks(y_ticks)

    # plt.show()
    plt.grid()
    plt.savefig(workpath+'/static/img/'+img_name+'.png')
    plt.clf()
    print("Done")



# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

# draw('zwtage_m.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)', 9, 44, 'wfg')
# draw('zwtage_f.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)', 9, 44, 'wwww')

# draw('zbmiage_f.csv', "BMI For Age", 'BMI (Kg)', 'Age (Month)', 16, 44, 'bfaaaa')
