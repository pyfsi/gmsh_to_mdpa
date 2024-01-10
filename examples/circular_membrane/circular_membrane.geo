// Gmsh project created on Thu Jul  8 17:53:33 2021
//+
r = DefineNumber[ 0.5, Name "Parameters/r" ];
//+
theta = DefineNumber[ 45, Name "Parameters/theta" ];
//Create centre
Point(1) = {0, 0, 0, 1.0};

//Create points on circle
For i In {2:9}
	Point(i) = {Cos((i-2)*Pi/180*theta), Sin((i-2)*Pi/180*theta), 0, 1.0};
EndFor

//Create lines
For i In {1:9}
	Line(i) = {1, i};
EndFor

//+
For i In {1:7}
	Circle(i+9) = {i+1,1, i+2};
EndFor

Circle(17) = {9, 1, 2};

//+
Curve Loop(1) = {2, 10, -3};
//+
Plane Surface(1) = {-1};
//+
Curve Loop(2) = {3, 11, -4};
//+
Plane Surface(2) = {-2};
//+
Curve Loop(3) = {4, 12, -5};
//+
Plane Surface(3) = {-3};
//+
Curve Loop(4) = {5, 13, -6};
//+
Plane Surface(4) = {-4};
//+
Curve Loop(5) = {6, 14, -7};
//+
Plane Surface(5) = {-5};
//+
Curve Loop(6) = {7, 15, -8};
//+
Plane Surface(6) = {-6};
//+
Curve Loop(7) = {8, 16, -9};
//+
Plane Surface(7) = {-7};
//+0
Curve Loop(8) = {9, 17, -2};
//+
Plane Surface(8) = {-8};
//+
Physical Surface("disc") = {3, 2, 1, 8, 7, 6, 5, 4};
//+
Physical Curve("edge") = {12, 13, 14, 15, 16, 17, 10, 11};
//+
Transfinite Curve {5, 4, 3, 2, 9, 8, 7, 6} = 50 Using Progression 1;
//+
Transfinite Curve {13, 12, 11, 10, 17, 16, 15, 14} = 50 Using Progression 1;
