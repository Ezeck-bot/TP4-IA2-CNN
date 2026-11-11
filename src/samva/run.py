
from pathlib import Path

import numpy as np  #pour un tableau multidimensionnel
import tensorflow as tf
from sklearn.model_selection import train_test_split

from samva.data_loader import NUM_CATEGORIES, load_data
from samva.model import get_model

# mes cosntantes
TEST_SIZE = 0.2
EPOQUES = 10

def main():

    dataset_path = Path("src/samva/data/gtsrb")

    try:
        # (a) charger vos données avec load_data
        print("Chargement des données...")
        images, labels = load_data(dataset_path)
    
        print(f"Nombre d'images chargées : {len(images)}")
        print(f"Nombre d'étiquettes chargées : {len(labels)}")

        images_array = np.array(images)

        # (b) transformer vos catégories en labels utilisables par les bibliothèques
        labels_array = tf.keras.utils.to_categorical(labels, num_classes=NUM_CATEGORIES)

        # (c) séparer les données en ensembles d’entraînement et ensembles de test
        print("Séparation des données (Train/Test)...")
        x_train, x_test, y_train, y_test = train_test_split(
            images_array, 
            labels_array, 
            test_size=TEST_SIZE,
            random_state=42
        )

        # (d) obtenir votre modèle avec get_model puis l’entraîner sur l’échantillon d’entraînement
        print("Création et entraînement du modèle...")
        model = get_model()

        # On lance l'entraînement
        model.fit(x_train, y_train, epochs=EPOQUES) #model.fit(x_train, y_train, epochs=EPOQUES, validation_split=0.1)

        # (e) tester le modèle avec l’échantillon de test
        print("\nÉvaluation du modèle sur l'échantillon de test...")
        loss, accuracy = model.evaluate(x_test, y_test, verbose=2)
        print(f"Soit : accuracy = {accuracy * 100:.2f}% - loss = {loss * 100:.2f}%")

        # (f) sauvegarder le modèle dans un fichier au format h5 ou keras
        model_save_filepath = Path("models/samva_model.keras")
        model_save_filepath.parent.mkdir(exist_ok=True) # pour créer le dossier 'models' s'il n'existe pas
        print(f"Sauvegarde du modèle dans {model_save_filepath}...")
        model.save(model_save_filepath)

        print("\n\n Entraînement terminé avec succès !")

    except FileNotFoundError as e:
        print(f"Erreur de fichier : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()