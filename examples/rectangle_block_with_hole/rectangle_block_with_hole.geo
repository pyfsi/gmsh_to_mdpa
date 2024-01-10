
//+
SetFactory("Built-in");
//+
r = DefineNumber[ 0.5, Name "Parameters/r" ];
//+
theta = DefineNumber[ 45, Name "Parameters/theta" ];

//Centre
Point(1) = {0, 0, 0, 1.0};

//Inner circle
Point(2) = {r*Cos(0*Pi/180*theta), r*Sin(0*Pi/180*theta), -0, 1.0};
Point(3) = {r*Cos(1*Pi/180*theta), r*Sin(1*Pi/180*theta), -0, 1.0};
Point(4) = {r*Cos(2*Pi/180*theta), r*Sin(2*Pi/180*theta), -0, 1.0};
Point(5) = {r*Cos(3*Pi/180*theta), r*Sin(3*Pi/180*theta), -0, 1.0};
Point(6) = {r*Cos(4*Pi/180*theta), r*Sin(4*Pi/180*theta), -0, 1.0};
Circle(1) = {2, 1, 3};
Circle(2) = {3, 1, 4};
Circle(3) = {4, 1, 5};
Circle(4) = {5, 1, 6};

//Outer circle
Point(7) = {2*r*Cos(0*Pi/180*theta), 2*r*Sin(0*Pi/180*theta), -0, 1.0};
Point(8) = {2*r*Cos(1*Pi/180*theta), 2*r*Sin(1*Pi/180*theta), -0, 1.0};
Point(9) = {2*r*Cos(2*Pi/180*theta), 2*r*Sin(2*Pi/180*theta), -0, 1.0};
Point(10) = {2*r*Cos(3*Pi/180*theta), 2*r*Sin(3*Pi/180*theta), -0, 1.0};
Point(11) = {2*r*Cos(4*Pi/180*theta), 2*r*Sin(4*Pi/180*theta), -0, 1.0};
Circle(5) = {7, 1, 8};
Circle(6) = {8, 1, 9};
Circle(7) = {9, 1, 10};
Circle(8) = {10, 1, 11};

//Outer square
//Corner points
Point(12) = {4*r, 0, -0, 1.0};
Point(13) = {4*r, 4*r, -0, 1.0};
Point(14) = {-4*r, 4*r, -0, 1.0};
Point(15) = {-4*r, 0, -0, 1.0};

// projection points
Point(16) = {4*r, 2*r*Sin(1*Pi/180*theta), -0, 1.0};
Point(17) = {2*r*Cos(1*Pi/180*theta), 4*r, -0, 1.0};
Point(18) = {2*r*Cos(2*Pi/180*theta), 4*r, -0, 1.0};
Point(19) = {2*r*Cos(3*Pi/180*theta), 4*r, -0, 1.0};
Point(20) = {-4*r, 2*r*Sin(3*Pi/180*theta), -0, 1.0};

//+
Line(9) = {2, 7};
//+
Line(10) = {7, 12};
//+
Line(11) = {12, 16};
//+
Line(12) = {16, 13};
//+
Line(13) = {13, 17};
//+
Line(14) = {17, 18};
//+
Line(15) = {18, 19};
//+
Line(16) = {19, 14};
//+
Line(17) = {15, 20};
//+
Line(18) = {11, 15};
//+
Line(21) = {5, 10};
//+
Line(22) = {4, 9};
//+
Line(23) = {9, 18};
//+
Line(24) = {10, 19};
//+
Line(25) = {8, 17};
//+
Line(26) = {8, 16};
//+
Line(27) = {10, 20};
//+
Line(28) = {6, 11};
//+
Line(29) = {20, 14};

//+
Line(30) = {3, 8};
//+
Curve Loop(1) = {18, 17, -27, 8};
//+
Plane Surface(1) = {1};
//+
Curve Loop(4) = {24, -15, -23, 7};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {23, -14, -25, 6};
//+
Plane Surface(5) = {5};
//+
Curve Loop(8) = {26, -11, -10, 5};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {30, -5, -9, 1};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {22, -6, -30, 2};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {21, -7, -22, 3};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {8, -28, -4, 21};
//+
Plane Surface(12) = {12};
//+
Transfinite Curve {4, 3, 2, 1} = 10 Using Progression 1;
//+
Transfinite Curve {8, 7, 6, 5} = 10 Using Progression 1;
//+
Transfinite Curve {28, 21, 22, 30, 9} = 20 Using Progression 1.05;
//+
Transfinite Curve {18, 27, 24, 23, 25, 26, 13, 16, 29, 10} = 10 Using Progression 1;
//+
Transfinite Curve {12} = 10 Using Progression 1;
//+
Curve Loop(13) = {27, 29, -16, -24};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {25, -13, -12, -26};
//+
Plane Surface(14) = {14};
//+
Transfinite Curve {15, 14} = 10 Using Progression 1;
//+
Transfinite Curve {17} = 10 Using Progression 1;
//+
Transfinite Curve {11} = 10 Using Progression 1;
//+
Transfinite Surface {13} = {20, 14, 19, 10};
//+
Transfinite Surface {1} = {15, 20, 10, 11};
//+
Transfinite Surface {12} = {6, 11, 10, 5};
//+
Transfinite Surface {11} = {5, 10, 9, 4};
//+
Transfinite Surface {10} = {3, 4, 9, 8};
//+
Transfinite Surface {9} = {7, 2, 3, 8};
//+
Transfinite Surface {8} = {12, 7, 8, 16};
//+
Transfinite Surface {14} = {8, 17, 13, 16};
//+
Transfinite Surface {5} = {8, 9, 18, 17};
//+
Transfinite Surface {4} = {9, 10, 19, 18};

//+
Recombine Surface {13, 4, 5, 14, 8, 9, 10, 11, 12, 1};
//+
Extrude {0, 0, 0.1} {
  Surface{13}; Surface{4}; Surface{5}; Surface{14}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Surface{1}; Layers{1}; Recombine;
}

Physical Volume("block") = {4, 3, 2, 1, 10, 9, 8, 7, 6, 5};
//+
Physical Surface("top") = {109, 87, 65, 47};

Physical Surface("bottom") = {135, 157, 219, 237};
//+
Physical Surface("left") = {113, 131};
//+
Physical Surface("right") = {43, 241};
//+
Physical Surface("hole") = {161, 183, 205, 223};

//+Reverse normal top faces
ReverseMesh Surface {109, 87, 65, 47};

//+Reverse normal left faces
ReverseMesh Surface {113, 131};;

//+Reverse normal right faces
ReverseMesh Surface {43, 241};

//+Reverse normal some bottom faces
ReverseMesh Surface {135, 157, 237};

//+Reverse normal some hole faces
ReverseMesh Surface {161, 183, 205};

//+Reverse normal some side faces
ReverseMesh Surface {118, 96, 74, 52, 250, 228, 206, 184, 162, 140};
