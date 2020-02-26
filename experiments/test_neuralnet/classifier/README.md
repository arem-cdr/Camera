# Commands to train classifier

/usr/bin/opencv_annotation --annotations=info.dat --images=p/
/usr/bin/opencv_createsamples -info info.dat -vec t.vec
/usr/bin/opencv_traincascade -data trained -vec t.vec -bg bg.txt -numNeg 38 -numPos 85 -numStages 20