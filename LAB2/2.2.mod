/*********************************************
 * OPL 22.1.2.0 Model
 * Author: szymo
 * Creation Date: 18 mar 2026 at 17:33:07
 *********************************************/
int n = ...;
int m = ...;

range r1 = 1..n;
range r2 = 1..m;

int S[r1] = ...;
int D[r2] = ...;


dvar int+ x[r1][r2];
int k[r1][r2] = ...;

minimize
  sum(i in r1, j in r2) x[i][j]*k[i][j];
  
subject to {
  forall(j in r2) sum( i in r1 ) x[i][j] == D[j];
  forall(i in r1) sum( j in r2 ) x[i][j] == S[i];
}