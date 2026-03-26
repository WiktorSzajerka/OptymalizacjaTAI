/*********************************************
 * OPL 22.1.2.0 Model
 * Author: Administrator
 * Creation Date: 25 mar 2026 at 18:31:37
 *********************************************/
/*********************************************
 * OPL 22.1.2.0 Model
 * Author: Mikołaj
 * Creation Date: 21 mar 2026 at 22:49:03
 *********************************************/

 int objectsNumber = ...;
 range objectsRange = 1..objectsNumber;
 
 float values[objectsRange][1..3] = ...;
 int size = ...;
 dvar float backpackAFill [objectsRange];
 dvar float backpackBFill [objectsRange];
 

 maximize sum(j in objectsRange) values[j][1] * (backpackAFill[j] + backpackBFill[j]);
 
 
 subject to {
   sum (i in objectsRange) ((backpackAFill[i] * values[i][2]) +  (backpackBFill[i] * values[i][3])) <= size;
   forall(i in objectsRange) (backpackAFill[i] >= 0.2 || backpackAFill[i] == 0);   
   forall(i in objectsRange) (backpackBFill[i] >= 0.2 || backpackBFill[i] == 0);
   forall(i in objectsRange) backpackAFill[i] + backpackBFill[i] <= 1;
 }
 
 execute {
   writeln("Size is: ", size);
   	for (var i =1; i<= objectsNumber; i++) {
   	   writeln("For object ", i, " Backpack A fill: ", backpackAFill[i]," size taken: ", backpackAFill[i] * values[i][2] , " value added: ", backpackAFill[i] * values[i][1]," , Backpack B fill: ", backpackBFill[i]," size taken: ", backpackBFill[i] * values[i][3], " value added: ", backpackBFill[i] * values[i][1]);
   	}
 }