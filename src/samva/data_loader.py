from pathlib import Path

import cv2  #le module OpenCV-Python (cv2)
import numpy as np  #pour un tableau multidimensionnel

# mes cosntantes
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
NORMALISE = 1.0

#fonction load_data qui retourne les images correspondantes aux étiquettes correspondantes
def load_data(dataset_path: Path) -> tuple[list[np.ndarray], list[int]]:
    """
    Charge les images et les étiquettes depuis le dossier dataset_path
    """

    images = []
    labels = []

    # 1. Boucler sur chaque catégorie (dossier 0 à 42)
    for category in range(NUM_CATEGORIES):
        # Construire le chemin vers le dossier de la catégorie
        category_path = Path(dataset_path / str(category))

        # Vérifier si le dossier existe
        if not category_path.is_dir():
            continue

        #je boucle sur chaque fichier dans le dossier et verifie sur le fichier à la bonne extension
        for filename in category_path.iterdir():
            if not filename.name.endswith(".ppm"):
                continue

            #je lis l'image
            image = cv2.imread(str(filename))

            #je resize l'image
            resize_image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            # Normalisation valeurs entre 0 et 1
            resize_normalize = cv2.normalize(resize_image, None, alpha=0, beta=NORMALISE, norm_type=cv2.NORM_MINMAX)

            #on l'ajoute au tableau
            images.append(resize_normalize)

            #on ajouter l'étiquette
            labels.append(category)
    
    return images, labels