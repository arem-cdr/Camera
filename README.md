# :video_camera: Caméra


**Merci de DL le zip. Des vidéos pour tester les algos sont incluses**

------------------------------------------------------------------------------------------
**Scripts qui marchent:**

- simple.py (détecte les polygônes à l'image et affiche leur position)
- distance.py (détecte les deux aruco à l'image et calcule la distance entre eux, la distance est exprimée en pixel)

**Scripts en cours de dev:**

- perspectivefix.py (cherche à corriger la perspective d'une caméra en utilisant une calibration initiale à l'aide de 4 aruco)

  - [x] Regarder à https://answers.opencv.org/question/136796/turning-aruco-marker-in-parallel-with-camera-plane/
  
  - [ ] Recup correctement les coins du rectangle formé par les 4 aruco
  
  - [ ] Effectuer la correction avec les fonctions getPerspectiveTransform() & warpPerspective()

**Scripts pas encore dev**

- combine_deux_camera.py
- goblet.py
- goblet_allongé.py
- girouette.py

**Script poubelle:**

- main_old.py
------------------------------------------------------------------------------------------
**:trophy: But** 

- extraire la position de nos robots
- extraire la position des robots ennemis
- extraire la position des gobelets
- extraire la position des gobelets allongés 
- extraire l'information sur la girouette

**:bookmark_tabs: plan d'action**

1. Parvenir à faire chaque tâche indépendament des autres
2. Combiner le tout en un seul script

