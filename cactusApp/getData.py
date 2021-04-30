import csv
import matplotlib.pyplot as plt
import numpy as np


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
    with open(f'{file_path}') as csv_file:
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
# data\zwtage_m.csv'
# x = np.array([0, 6])
# y = np.array([0, 250])
# y1 = np.array([3, 100])
#
# plt.axis([5, 20, 20, 40])
# plt.plot(x, y)
def draw(data, title, y_lable, x_lable):
    age, p1, p2, p3, p4, p5, p6, p7, p8 = getData(data)
    plt.plot(age, p1, label='p1')
    plt.plot(age, p2, label='p2')
    plt.plot(age, p3, label='p3')
    plt.plot(age, p4, label='p4')
    plt.plot(age, p5, label='p5')
    plt.plot(age, p6, label='p6')
    plt.plot(age, p7, label='p7')
    plt.plot(age, p8, label='p8')

    plt.title(title)
    plt.ylabel(y_lable)
    plt.xlabel(x_lable)

    plt.legend()

    x_ticks = np.arange(24, 60, 2)
    plt.xticks(x_ticks)

    y_ticks = np.arange(5, 50, 2)
    plt.yticks(y_ticks)

    # plt.show()
    plt.grid()
    plt.savefig('static/img/f1.png')
    # fig.savefig('path/to/save/image/to.png')

draw('data\zwtage_m.csv', "Weight For Age", 'Weight (Kg)', 'Age (Month)')
