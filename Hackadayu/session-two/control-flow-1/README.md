# Control Flow
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

