# :video_camera: Caméra



                                           Camera     Xbee
                                               Raspberry
                                              _________
                                                |   |
                                                |   |
                                                |   |
                                                |   |   Système de repérage
                                                |   |   central
                                                |   | 
                                                |   |
              _______                           |   |
             |       |                          |   |
             | Robot |       |--|               |   | 
             |_______|       |__|               |___|
             

------------------------------------------------------------------------------------------
**:trophy: Objectifs** 

- extraire la position de nos robots
- extraire la position des robots ennemis
- extraire la position des gobelets
- extraire la position des gobelets allongés 
- extraire des informations sur l'état des actions.
- extraire l'information sur la girouette
- envoyer les infomations extraites par la Xbee




**:bookmark_tabs: Plan d'action**

1. Parvenir à faire chaque tâche indépendament des autres
2. Combiner le tout en un seul script avec des élements modulaires

------------------------------------------------------------------------------------------
**:hammer: Démarrage rapide** 

  #### 1. Installez pip
  ```apt-get install python3-pip```

  #### 2. Installez virtualenv
  ```pip3 install virtualenv```

  #### 3. Créez un virtualenv
  ```virtualenv -p python3 obelix```

  #### 4. Activez le virtualenv
  ```source obelix/bin/activate```

  #### 5. Téléchargez les libraries
  ```pip3 install -r requirements.txt```

------------------------------------------------------------------------------------------
# Documentation

**Liste des modules qui peuvent être chargés dans main.py**

- Calibrator.py

  Uses 4 ARUCO ID and the dimension of the rectangle formed by them in the real life.
  Gives you a bird point of view.


- fisheye.py 
  
  Uses matricies calculated by fisheye_calculator.py to fix distortion
  
  
- gextractor.py 
  
  Uses a succession of filters and image processing technics to extract the objects. 
  Please use the debug function to tweak the parameters of the extractor.
  
  
 - gextractorNG.py
  
  Uses a background difference method to extract objects. Takes the background img when initialized.
  
 ------------------------------------------------------------------------------------------ 
 **Autres scripts :**
 
  - test_camera.py

    Small module to test if opencv and the camera are working.
    
------------------------------------------------------------------------------------------
**:hammer: Redémarrage sur le script** 

#### 1. Accès à /etc/rc.local
  ```sudo -i```
  
  ```nano /etc/rc.local```
  
#### 2. Modifiez /etc/rc.local
  ``` exec 1>/tmp/rc.local.log 2>&1 
      set -x
      su pi -c "cd /home/pi/Documents/obelix/Camera/obelix && python3 main.py"  &
      exit 0
  ```

------------------------------------------------------------------------------------------

 **Communication :**



| Catégorie| Niveau encapsulation | Valeur | Informations transmises | Séquence après valeur | Fin de séquence |
|----------|---------|---------|-------------------------|----------------|-----------------|
| Objet | 1 |  -101 | Obstacle perçu  | Objet 1 | -1 |
| Objet 1 | 2 | 1 | Gobelets vert | (int int) n_fois | -1 |
| Objet 1 |  2 | 2 | Gobelets rouge | (int int) n_fois  | -1 |
| Objet 1 |  2 | 3 | Robot | (int int) n_fois | -1 |
| Actions | 1 | -150 | Action realise | (int) n_fois | -1 |

**Exemples valides:**

- -101 1 X1 Y1 2 X2 Y2 1 X3 Y3 -1 // Gobelet vert(X1,Y1) , Gobelet rouge(X2,Y2) , Gobelet vert(X3,Y3)
- -150 A1 A2 A3 -1 // Actions A1, A2, A3 réalisées

------------------------------------------------------------------------------------------

 **GPIO :**

 | Numéro | Nom | Description
|----------|-------------|----------------------------------------------|
| 15 | Switch| Passer d'un mode à l'autre |
| 23 | FPS rate  | Vérifier la vitesse d'execution du workflow |
| 18 | Diode Jaune | Active lorsque config en mode jaune |
| 14 | Diode Bleue | Active lorsque config en mode bleu |
| 20 | Diode Blanche | Active pendant la période de calibration (fonctionne comme un radar de recul) |
| 21 | Diode Blanche | Active pendant la période de calibration (fonctionne comme un radar de recul) |
  


