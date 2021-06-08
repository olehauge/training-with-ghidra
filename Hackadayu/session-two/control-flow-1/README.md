# Control Flow
For this challenge we were to:
- find the number of compare statements in main, 
- what the three values being compared are, 
- and see if it is possible to pass all the checks. 

## Fixing syntax
For this session we learned that we can modify a functions signature, and how this could improve the decompiled C-code. 
For this challenge I changed the main function signature from ```undefined8 main(int param_1,long param_2)``` to ```int main(int argc,char **argv)```. 
This way it is defined with the C-standard argument counter ```int argc``` and argument vector ```char **argv```.

BEFORE CHANGE
```
undefined8 main(int param_1,long param_2)

{
  int iVar1;
  int iVar2;
  undefined8 uVar3;
  
  if (param_1 == 3) {
    iVar1 = atoi(*(char **)(param_2 + 8));
    iVar2 = atoi(*(char **)(param_2 + 0x10));
    if (iVar2 < iVar1) {
      if (iVar2 << 1 < iVar1) {
...
```
AFTER CHANGE
```
int main(int argc,char **argv)

{
  int iVar1;
  int iVar2;
  
  if (argc == 3) {
    iVar1 = atoi(argv[1]);
    iVar2 = atoi(argv[2]);
    if (iVar2 < iVar1) {
      if (iVar2 << 1 < iVar1) {
...
```
## Number of compare statements
There are 4 compares in total:
```        
00100699 83 7d ec 03     CMP        dword ptr [RBP + local_1c],0x3
0010069d 74 16           JZ         cmpOneOK
```
The first compares the ```argc``` variable which is stored at ```RBP + local_1c``` with 3. Meaning that we have to provide 2 arguments for the program to pass (given by ```JZ```). 
```       
001006ec 8b 45 f4        MOV        EAX,dword ptr [RBP + local_14]
001006ef 3b 45 f8        CMP        EAX,dword ptr [RBP + local_10]
001006f2 7f 13           JG         cmpTwoOK
```
The second compares the argument stored at ```RBP + local_14``` (ivar1) with the argument stored at ```RBP + local_10``` (ivar2) and checks if the result is greater than. The values that are compared here are the results of ```atoi``` functions. ```int atoi(const char *str)``` converts the string argument ```str``` to an integer (type int).
```
00100707 d1 65 f8        SHL        dword ptr [RBP + local_10],1
0010070a 8b 45 f8        MOV        EAX,dword ptr [RBP + local_10]
0010070d 3b 45 f4        CMP        EAX,dword ptr [RBP + local_14]
00100710 7d 13           JGE        cmpThreeOK
```
The third compares EAX with the value stored at ```RBP + local_14```. EAX is the result of left shifitng (SHL) the value stored at ```RBP + local_10``` by one. 
If the result is greater than or equal, it goes to the last check.

NOTE: Left shifting a value by 1 is the equivalent of doubling the value. 
```
0010072b 83 f8 63        CMP        EAX,0x63
0010072e 7f 13           JG         cmpFourOK=SUCCESS
```
The fourth compares the value stored in ```EAX``` to ```0x63/99```. EAX is the result of the addition of the values at address ```RBP + local_14``` and ```RBP + local_10``` before subtracting ```RBP + local_14``` from the value. Basically, we end up with ivar2. If the result is greater than the program will call the success string. 

## Passing all the checks
- The fourth check has to have a value greater than ```99``` to pass e.g. the ivar2.
- The third check has to have the var2 leftshifted once be greater than or equal var1. This means that the second argument has to be at least half the size of the first argument. 
- The second check has to have the var1 greater than var2. 
- The first check has to have the program executed with two arguments.

This means that the minimum value of the second argument has to be 100 and the first has to be at least one increment bigger: 101. Testing this with the program yields the following result: 
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-two/exercises# ./control-flow-1 101 100
Proper values provided! Great work!
```
