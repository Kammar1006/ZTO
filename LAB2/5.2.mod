/*********************************************
 * OPL 22.1.2.0 Model
 * Author: szymo
 * Creation Date: 25 mar 2026 at 17:16:46
 *********************************************/

 int n = ...;
 range r1 = 1..n;
 float a[r1] = ...;
 float b[r1] = ...;
 float r[r1] = ...;
 
 float f[r1][r1] = ...;
 
 dvar float+ x[r1];
 dvar float+ y[r1];
 dvar float+ d[r1][r1];
 
 minimize
  sum(i in r1, j in r1) f[i][j]*d[i][j];
  
subject to {
  forall(i in r1, j in r1) d[i][j]^2 >= (x[i]-x[j])^2+(y[i]-y[j])^2;
  forall(i in r1) r[i]^2 >= (x[i]-a[i])^2+(y[i]-b[i])^2;
}