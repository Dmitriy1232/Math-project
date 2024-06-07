import tkinter as tk
import random
import numpy as np
import matplotlib.pyplot as plt

#сумма квадратов списка
def sum_sqr(x):
    sum = 0
    for i in x:
        sum += i*i
    return sum

#генерация списков
def generate_arrays(size):
    array = [random.randint(0, 100) for _ in range(size)]

    return array


def linear_regression():

    #заполнения массива в зависимости от режима
    if random_mode.get() == 1:
        x_array = generate_arrays(int(random_array_entry.get()))
        y_array = generate_arrays(int(random_array_entry.get()))
    else:
        x_array = [float(i) for i in x_array_entry.get().split(' ')]
        y_array = [float(i) for i in y_array_entry.get().split(' ')]

    n = len(x_array)

    #решение матричное и не матричное
    if matrix_mode.get() == 1:
        X = np.matrix([np.ones((len(x_array))), x_array]).T
        y = np.matrix(y_array).T

        #решение по матричной формуле
        coef = (X.T * X)**-1 * X.T * y

        b0 = float(coef[0])
        b1 = float(coef[1])
    else:

        sum_xy = sum([x_array[i] * y_array[i] for i in range(n)]) #сумма x*y

        # решение системы уровнений
        a = np.array([[sum(x_array), n],
                      [sum_sqr(x_array), sum(x_array)]])
        b = np.array([sum(y_array),
                      sum_xy])
        coef = np.linalg.solve(a,b)

        b1 = float(coef[0])
        b0 = float(coef[1])

    #Вычисление K, Qx, Qy, r по формулам
    K = sum([x_array[i]*y_array[i] for i in range(n)])/n - sum(x_array)*sum(y_array)/n**2
    sx = (sum_sqr(x_array) /n - (sum(x_array)/n)**2)**0.5
    sy = (sum_sqr(y_array) / n - (sum(y_array) / n) ** 2) ** 0.5
    r = K/(sx*sy)

    #Создание текста
    if matrix_mode.get() == 1:
        canvas.create_text(5,5,anchor='nw',text=f'Данные:\n\n      X\n{X}\n\n    Y\n{y}')
        canvas.create_text(100, 5, anchor='nw', text=f"X' - транспонированная матрица X \n{X.T}\n\nX' * X\n{X.T*X}\n\n(X' * X)^-1\n{(X.T*X)**-1}\n\n(X' * X)^-1 * X'y\n{(X.T*X)**-1*X.T*y}\n\na = {b0:.2f}\nb = {b1:.2f}\nУравнение регресси: y = {b0:.2f} + {b1:.2f}x\nK xy = {K:.2f}\nQx = {sx:.2f}\nQy = {sy:.2f}\nr = {r:.2f}")
    else:
        canvas.create_text(100, 5, anchor='nw', text=f'a = {b0:.2f}\nb = {b1:.2f}\nУравнение регресси: y = {b0:.2f} + {b1:.2f}x\nK xy = {K:.2f}\nQx = {sx:.2f}\nQy = {sy:.2f}\nr = {r:.2f}')
    canvas.pack()

    #Создание графика
    plt.plot(x_array, y_array, 'ro')
    plt.title('График линейной регрессии')
    plt.ylabel('Продажи')
    plt.xlabel('Размер обуви')
    predict_array = [b0 + b1*i for i in x_array]
    plt.plot(x_array,predict_array)
    plt.show()

def on_submit():
    #Удаление ненужных объектов
    radio_non_random.destroy()
    radio_random.destroy()
    submit_button.destroy()

    #Создание новых полей в зависимости от выбранного режима
    if random_mode.get() == 0:
        x_array_lable.pack()
        x_array_entry.pack()
        y_array_lable.pack()
        y_array_entry.pack()
    else:
        random_array_lable.pack()
        random_array_entry.pack()
    radio_matrix.pack()
    radio_non_matrix.pack()

    colculet_button.pack()



# Создание всех элементов интерфейса
root = tk.Tk()
root.title("Linear Regression Calculator")
canvas = tk.Canvas(bg="white", width=500, height=500)
x_array_lable = tk.Label(text='X')
x_array_entry = tk.Entry()
y_array_lable = tk.Label(text='Y')
y_array_entry = tk.Entry()
random_array_lable = tk.Label(text='Задайте размер массивов')
random_array_entry = tk.Entry()
matrix_mode = tk.IntVar()
radio_matrix = tk.Radiobutton(root, text="Матрично", variable=matrix_mode, value=1)
radio_non_matrix = tk.Radiobutton(root, text="Не матрично", variable=matrix_mode, value=0)
colculet_button = tk.Button(root, text="Вычеслить", command=linear_regression)





#Создание стартовых кнопок и надписей
random_mode = tk.IntVar()
radio_random = tk.Radiobutton(root, text="Случайно", variable=random_mode, value=1)
radio_random.pack()
radio_non_random = tk.Radiobutton(root, text="Вручную", variable=random_mode, value=0)
radio_non_random.pack()

submit_button = tk.Button(root, text="Далее", command=on_submit)
submit_button.pack()

# Запуск окна
root.mainloop()