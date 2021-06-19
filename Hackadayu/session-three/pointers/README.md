# Pointers
For this challenge we were to:
- Find how many members there are in the struct
- Figure out what each member represents
- Explain how the pointers are used
- Find the correct password

## Struct members and representation
The struct consists of the ```key```, ```username``` and ```password``` values. 

## Initial analysis of the program
The program takes 3 arguments: ```key```, ```username``` and ```password```. 
It has 6 "main" compares:
1. 3 arguments has to be provided.
2. The ```key``` value has to be integer.
3. The ```username``` has to be less than ```0x255```.
4. The ```username``` has to be longer than ```0x7```.
5. The ```password``` has to be less than ```0x255```.
6. The ```password``` has to be longer than ```0x7```.

After passing the checks the three functions are called:
1. ```keyCalc```: Adds what is stored at ```RBP + 0xbeef``` to the ```key``` value.
2. ```swapNames```: Swaps the values stored at two addresses. I think these are the addresses of the ```key``` and ```username```, but I will have to check this in GDB.
3. ```gen_password```: Presumably uses the swapped values to XOR them and do some additional arithmetic before returning a new "password reference".

The password is then looped through and compared to the template. It does however seem to compare the value at the username address to the value at the stored address.
I assume this is due to the swapped memory addresses, but this will become more clear after using GDB. 

If the while loop does not fail we are greated by the success string: "Correct! Access granted!"

## GDB analysis

## Learning notes
- Functions can be stored in pointers and ran at a later point: 
```
00400857 48 c7 45        MOV        qword ptr [RBP + stored_keyCalcAddress],keyCalc
         e0 95 06 
         40 00
...
00400873 ff d0           CALL       RAX=>keyCalc                                    
```
