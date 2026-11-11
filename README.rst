A lire obligatoire avant toute utilisation de ce projet.

Les dossiers 0 à 42 contenanat les fichiers `.ppm` doivent être placés dans le dossier `gtsrb` qui se trouvre dans `src/samva/data/`. Le dossier `gtsrb` doit être créé si il n'existe pas.

Puis la commade `uv init` doit être exécutée
Ensuite la commade `uv sync`
Puis faire `uv run samva` pour lancer le projet.

De base dans `model.py` le sytème fonctionne avec deux conv2D et deux maxpooling2D. 
Pour améliorer la précision, il est possible d'ajouter un conv2D et un maxpooling2D supplémentaire. 
Il faut pour cela décommenter les lignes 39 et 40 dans `model.py` et commenter les lignes 37 et 38.