from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, Input, MaxPooling2D
from tensorflow.keras.models import Model, Sequential

from samva.data_loader import IMG_HEIGHT, IMG_WIDTH, NUM_CATEGORIES

# mes cosntantes
FILTERS = 32 # nombre de filtres pour la couche de convolution
DROPOUT = 0.5 #`0.5` soit 50% des neurones évités pour empêcher le surapprentissage
POOL_SIZE = (2, 2)
KERNEL_SIZE = (2, 2)

"""
Crée un modèle de réseau de neurones convolutifs (CNN) pour la classification d'images.
Le Convolutional Neural Network comprens plusierus couches. De façon simle :
- La première couche est une couche de convolution (Conv2D) qui applique des filtres pour extraire des caractéristiques de l'image.
- La deuxième couche est une couche de pooling (MaxPooling2D) qui réduit la taille pour garder seulement l'information la plus importante (ça allège les calculs)
- La troisième couche est une couche de flatten (Flatten) "Aplatit" l'image 2D en une longue liste 1D pour la préparer à la classification
- La quatrième couche est une couche dense (Dense) est Le "cerveau" qui prend la liste et essaie de deviner la catégorie.
- La cinquième couche est une couche de dropout (Dropout) qui aide à prévenir le surapprentissage en oubliant volontairement certains neurones pendant l'entraînement pour éviter qu'il n'apprenne "par cœur"
"""

#fonction get_model qui retourne un mode de de réseau de neurones convolutifs (CNN) pour la classification d'images
def get_model() -> Model:
    """
    Crée un modèle de réseau de neurones convolutifs (CNN) pour la classification d'images.
    """
    model = Sequential()

    #Block 1 : Détection des motifs simples (bords, couleurs) et réduction de la taille de moitié
    model.add(Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3))) # au lieu de faire `, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)` dans Conv2D
    model.add(Conv2D(FILTERS, KERNEL_SIZE, activation='relu')) 
    model.add(MaxPooling2D(pool_size=POOL_SIZE))

    #Block 2 : détecte les motifs plus complexes (formes, textures) et réduction de la taille de moitié
    model.add(Conv2D(FILTERS * 2, KERNEL_SIZE, activation='relu'))
    model.add(MaxPooling2D(pool_size=POOL_SIZE))

    #Block 3 : détecte les motifs encore plus complexes (objets, parties d'objets) et réduction de la taille de moitié
    # model.add(Conv2D(FILTERS * 3, KERNEL_SIZE, activation='relu'))
    # model.add(MaxPooling2D(pool_size=POOL_SIZE))

    # #Block 4 : détecte les motifs encore plus complexes (objets, parties d'objets) et réduction de la taille de moitié
    # model.add(Conv2D(FILTERS * 4, KERNEL_SIZE, activation='relu'))
    # model.add(MaxPooling2D(pool_size=POOL_SIZE))

    # Applatir pour les couches denses
    model.add(Flatten())

    # Couches denses avec Dropout
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(DROPOUT))

    #Dense
    model.add(Dense(NUM_CATEGORIES, activation='softmax')) #je mets softmax pour que la sortie soit une probabilité pour chaque catégorie, la somme des probabilités est égale à 1.

    #compile le modèle avec la fonction de perte, l'optimiseur et les métriques
    model.compile(
        loss='categorical_crossentropy', 
        optimizer='adam', 
        metrics=['accuracy'])

    return model