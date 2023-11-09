import os
import json

def linear_regression():
    km = input("Entrez un kilomètrage:\n")
    if km.isdigit():
        if os.path.exists('data.json'):
            with open('data.json', 'r') as json_file:
                existing_data = json.load(json_file)
                theta0 = existing_data['theta0']
                theta1 = existing_data['theta1']
                json_file.close()
        else :
            with open('data.json', 'w') as json_file:
                json.dump({'theta0': '0', 'theta1' : '0'}, json_file)
                json_file.close()

    else:
        print("Merci d entrer une valeur chiffrée")
        exit()

        
if __name__ == '__main__':
    linear_regression()