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

  - Installez Opencv, imutils, numpy et pyyaml.
  - Lancez main.py.

------------------------------------------------------------------------------------------

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

 **Communication :**



| Catégorie| Valeur | Informations transmises | Fin de séquence |
|----------|--------|-------------------------|-----------------|
| Objet | -101 | Obstacles perçu  | -1 |
| Objet | 1 | Gobelet vert | -1 |
| Objet | 2 | Gobelet rouge | -1 |
| Objet | 3 | Robot | -1 |

Exemple valide:

-101 1 X1 Y1 2 X2 Y2 1 X3 Y3 -1

------------------------------------------------------------------------------------------

 **GPIO :**

 | Numéro | Name | Description
|----------|-------------|----------------------------------------------|
| 15 | Switch| Passer d'un mode à l'autre |
| 23 | FPS rate  | Vérifier la vitesse d'execution du workflow |
| 18 | Diode Jaune | Active lorsque config en mode jaune |
| 14 | Diode Bleue | Active lorsque config en mode bleu |

  


