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
What does the different functions actually do? I used the following input for testing:
````
run $(python -c 'print("12345678 \x41\x41\x41\x41\x42\x42\x42\x42 \x43\x43\x43\x43\x44\x44\x44\x44")')
````
### keyCalc
Using GDB I can verify that the function:
1. Takes two input arguments: ```EDI``` (the ```key``` value: ```12345678```) and ```ESI``` (the value stored at ```RDX + 0xbeef```: ```12394557```).
2. Adds the two values together: ```12345678 + 12394557 = 24740235```
3. Left shifts the reuslt 3 times (same as multiplying with 8), which gives: ```197921880``` or ```0xbcc0c58```.

### swapNames
Using GDB I can verify that the function:
1. Takes two input arguments: ```RDI``` == the address ```0x7ffd65516db8``` and ```RSI``` == the address ```0x7ffd65516dc0```. 
2. Allocates memory on the heap and return the address for the memory in ```RAX```.
3. Stores the ```0x7ffd65516db8``` address to ```RAX```.
4. Takes the last byte (```0x7e```) of the value, ```0x6551787e``` stored at ```0x7ffd65516db8```, and stores it in ```rbp-0x8```.
5. Stores the ```0x7ffd65516dc0``` address to ```RAX```.
6. Takes the last byte (```0x87```) of the value, ```0x65517887``` stored at ```0x7ffd65516dc0```, and stores it in ```edx```.
7. Then sets ```RAX``` to ```0x7ffd65516dc0```.
8. Moves ```DL``` to ```RAX```.
9. Then sets ```RAX``` to ```rbp-0x8``` and moves it to ```edx```.
10. ```RAX``` is then set to ```0x7ffd65516dc0```.
11. Moves ```DL``` to ```RAX```.

In short, it switches the pointers to the values stored at the given address locations.

### gen_password
Using GDB I can verify that the function:
1. Takes the ```key``` value in the ```RDI``` register and stores it in a local variable ```[rbp-0x18]```.
2. Takes the first byte of the ```password``` value and stores it in ```RAX```, which equates to ```\x43\x43\x43\x43```. 
3. ```RAX``` is used to calculate the ```strlen``` for the byte, which equates to ```8```, and stores it in a local variable ```[rbp-0xc]```.
4. The lenght value is then used to allocate memory on the heap with ```malloc```, returning a pointer to the memory address. 
5. Then we enter a while loop that runs for the length stored at ```[rbp-0xc]```. It does:
   -  It gets the ```password``` value at ```[rax+0x8]``` by setting the ```RAX``` register to contain the ```key``` value address. 
   -  It then adds the ```counter``` value to the address to get the current iteration char and stores it in the ```ECX``` register.
   -  It then stores the ```key``` value (not address) in ```EAX```.
   -  Before adding ```ECX``` and ```EAX``` together. For the first iteration this would look like: ```0xbc614e + 0x43 = 0xbc6191```.
   -  It then stores the ```keyCalc``` result value: ```0xbcc0c58``` from ```rax+0x18``` in ```EAX```, where ```RAX``` is first set to ```rbp-0x18```.  
   -  The ```EAX``` value is then XORed with the ```ECX``` value. e.g. ```0xbcc0c58 xor 0xbc6191 = 0xb706dc9```. 
   -  The last byte ```0xc9``` (AL) of the ```0xb706dc9``` XOR-result is stored.
   -  The ```counter``` value is then added to the address of ```0xc9```. 
   -  The same is repeated again.
   -  The result of which is added to ```-0x13```, of which the last bytes (AL) ```0xb6``` is stored in memory
   -  The loop repeats this until the counter equals the length stored at ```[rbp-0xc]```.
   -  The result is a string of XORed values.

With my input of ```key``` = ```12345678``` and ```password``` = ```\x43\x43\x43\x43\x44\x44\x44\x44``` I got the following result: ```\xb6\xb6\xb6\xb6\xb7\xb7\xb7\xb7```. I reversed the function in Python as well (code is supplied above).

### Code after compares and functions 
The rest of the program consists of a loop that loops through the the XORed-result character by character and compares them to the corresponding characters in the ```username``` value. With my input this meant 8 iterations. 


### Success string
In GDB:
```
run $(python -c 'print("12345678 \xb6\xb6\xb6\xb6\xb7\xb7\xb7\xb7 \x43\x43\x43\x43\x44\x44\x44\x44")'
```
or from terminal:
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./pointers $(python -c 'print("12345678 \xb6\xb6\xb6\xb6\xb7\xb7\xb7\xb7 \x43\x43\x43\x43\x44\x44\x44\x44")')
Correct! Access granted!
```

## Learning notes
- Functions can be stored in pointers and ran at a later point: 
```
00400857 48 c7 45        MOV        qword ptr [RBP + stored_keyCalcAddress],keyCalc
         e0 95 06 
         40 00
...
00400873 ff d0           CALL       RAX=>keyCalc                                    
```
- Arguments are passed to functions using the registers, where the 1st argument uses ```RDI``` and the second uses ```RSI```. [More info here](http://6.s081.scripts.mit.edu/sp18/x86-64-architecture-guide.html).
