import csv
import matplotlib.pyplot as plt
import os.path
import pandas as pd
import json


def train():
    data = pd.read_csv("data.csv")
    learning_rate = 0.1
    m = len(data.km.values)
    the0 = 0.0
    the1 = 0.1
    min_km = min((data.km))
    max_km = max((data.km))
    max_price = max((data.price))
    min_price = min((data.price))
    for i in range(1000):
        sum_t0 = 0.0
        sum_t1 = 0.0
        for value in data.values:
            #Utilisation de la normalisation selon la formule: X_norm = (X - X.min()) / (X.max() - X.min())
            #La normalisation est utile pour reduire l ecart entre les donnees en les contenant toutes entre 0 et 1. Un trop grand ecart peut fausser l apprentissage.
            value_0 = (float(value[0]) - min_km) / (max_km - min_km)
            value_1 = (float(value[1]) - min_price) / (max_price - min_price)
            #On additionne le total de nos erreurs dans la prediction du prix du vehicule pour se faire on applique la formule estimatePrice(mileage) = θ0 + (θ1 ∗ mileage) puis on soustrait le vrai prix pour comparer pour chaque index.
            sum_t0 = sum_t0 + (the0 + (the1 * value_0) - value_1)
            # Le calcul pour la sum_t1 est le meme mais on multiplie par le nombre de kilometres a la fin pour estimer la participation du kilometrage a notre erreur.
            sum_t1 = sum_t1 + (the0 + (the1 * value_0) - value_1) * value_0
        
        #Normalisation de learning_rate et calcul des valeurs temporaires de theta0 et theta1 en fonction de la marge d erreur trouvee.
        tmp_the0 = learning_rate * 1/m * sum_t0
        tmp_the1 = learning_rate * 1/m * sum_t1

        #Ajustement des valeurs initiales avant de reboucler sur les valeurs et continuer de les peaufiner encore et encore.
        the0 -= tmp_the0
        the1 -= tmp_the1

    #Denormalisation des donnees, pour les ramener a leur echelle initiale.
    the0 = the0 * (max_price - min_price) + min_price - (the1 * min_km * (max_price - min_price)) / (max_km - min_km)
    the1 = the1 * (max_price - min_price) / (max_km - min_km)

    with open('data.json', 'w') as json_file:
        json.dump({'theta0': the0, 'theta1' : the1}, json_file)
        json_file.close()

    print(f'Les valeurs ont été mises à jour, enregistrées dans le data.json et sont égales á theta0: {the0} et theta1: {the1}')

    plt.scatter(data['km'], data['price'])
    plt.title('Repartition du prix selon le kilometrage')
    #Tracage de la ligne de regression qui est la relation entre les deux variables.
    plot_x = data.km
    plot_y = the1 * plot_x + the0
    plt.plot(plot_x, plot_y, '-g')
    plt.xlabel('Kilometres')
    plt.ylabel('Prix')
    plt.show()
    
if __name__ == '__main__':
    if os.path.exists('data.csv'):
        train()