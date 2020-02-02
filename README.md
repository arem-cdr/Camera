# :video_camera: Caméra


------------------------------------------------------------------------------------------
**List of modules:**

- Calibrator.py

  Load a Calib Object with 4 ARUCO ID, and the dimension of the rectangle
  formed by them in the real life.
  Then you need to apply genCalibration() to the object with an image, 
  it will try to detect the ARUCO's in the image and will generate
  matricies representing the necessary transformation to go from the 
  camera plan to the aruco plan.
  Then to get the bird point of view, use applyCalibration() with an image and
  it will return you an image corresponding to the bird point of view.


- fisheye.py 
  
  Uses matricies calculated by fisheye_calculator.py to fix distortion
  
  
- gextractor.py 
  
  Uses a succession of filters and image processing technics to extract the objects. 
  Please use the debug function to tweak the parameters of the extractor.
  
  
 - gextractorNG.py
 
  Uses a background difference method to extract objects. Takes the background img when initialized.
  
 ------------------------------------------------------------------------------------------ 
 **Other scripts :**
 
  - test_camera.py

    Small module to test if opencv and the camera are working.
  
  
------------------------------------------------------------------------------------------
**:hammer: Building** 

  You only have to edit TEMP ZONES in main.py to interact with the tool.

------------------------------------------------------------------------------------------
**:trophy: Goal** 

- extraire la position de nos robots
- extraire la position des robots ennemis
- extraire la position des gobelets
- extraire la position des gobelets allongés 
- extraire l'information sur la girouette

**:bookmark_tabs: plan d'action**

1. Parvenir à faire chaque tâche indépendament des autres
2. Combiner le tout en un seul script

