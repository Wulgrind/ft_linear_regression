import csv
import matplotlib.pyplot as plt
import os.path
import pandas as pd
import json

def train():
    data = pd.read_csv("data.csv")
    learning_rate = 0.01
    m = len(data.km.values)
    the0 = 0.0
    the1 = 0.0
    overfit_reached = 0
    overfit = 0
    min_km = min((data.km))
    max_km = max((data.km))
    max_price = max((data.price))
    min_price = min((data.price))
    prev_the0_rounded = 0
    prev_the1_rounded = 0
    for i in range(100000):
        sum_t0 = 0.0
        sum_t1 = 0.0
        for value in data.values:
            value_0 = (float(value[0]) - min_km) / (max_km - min_km)
            value_1 = (float(value[1]) - min_price) / (max_price - min_price)
            sum_t0 = sum_t0 + (the0 + (the1 * value_0) - value_1)
            sum_t1 = sum_t1 + (the0 + (the1 * value_0) - value_1) * value_0
        
        tmp_the0 = learning_rate * 1/m * sum_t0
        tmp_the1 = learning_rate * 1/m * sum_t1

        the0 -= tmp_the0
        the1 -= tmp_the1

        the0_rounded = round(the0, 5)
        the1_rounded = round(the1, 5)

        if the0_rounded == prev_the0_rounded or the1_rounded == prev_the1_rounded:
            overfit += 1
        else :
            overfit = 0
        if overfit == 20:
            overfit_reached = 1
            print(f"Overfit detected, early stopping triggered after {i} loops")
        prev_the0_rounded = the0_rounded
        prev_the1_rounded = the1_rounded
        if overfit_reached == 1:
            break

    the0 = the0 * (max_price - min_price) + min_price - (the1 * min_km * (max_price - min_price)) / (max_km - min_km)
    the1 = the1 * (max_price - min_price) / (max_km - min_km)

    if os.path.exists('data.json'):
            with open('data.json', 'r') as json_file:
                old_data = json.load(json_file)
                old_theta0 = old_data['theta0']
                old_theta1 = old_data['theta1']
                json_file.close()

    with open('data.json', 'w') as json_file:
        json.dump({'theta0': the0, 'theta1' : the1}, json_file)
        json_file.close()

    print(f'Les valeurs ont été mises à jour, enregistrées dans le data.json et sont égales á theta0: {the0} et theta1: {the1}')

    plt.scatter(data['km'], data['price'])
    plt.title('Repartition du prix selon le kilometrage')
    plot_x = data.km.values
    plot_y = the1 * plot_x + the0
    plot_y_old = old_theta1 * plot_x + old_theta0
    plt.plot(plot_x, plot_y_old, '-r', label='Ancien modèle')
    plt.plot(plot_x, plot_y, '-g', label='Nouveau modèle')
    plt.xlabel('Kilometres')
    plt.ylabel('Prix')
    plt.show()
    
if __name__ == '__main__':
    if os.path.exists('data.csv'):
        train()