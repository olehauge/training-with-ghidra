# Structures
For this challenge we were to:
- Find the number of members
- Explain what the members represent
- Recreate the struct in Ghidra
- Get the right passcode

## Fixing syntax
- Change the main function signature to ```int main(int argc, char **argv)```. This makes the decompiled code more readable.
- Figure out what is compared (change labels) and what functions called:
    - 1: 3 values are supplied: Key, username, password
    - 2: The key value contains only numbers
    - 3: The username is shorter than 0x255
    - 4: The username is longer than 0x7
    - 5: The password is shorter than 0x255
    - 6: The password is longer than 0x7
    - 7: Call ```add()```
    - 8: Call ```gen_password()```
    - 7: While loop compare => Success 
    
## Finding the members and what they represent.
The struct seems to consist of 3 members: key, username, password. These values are stored from ```argv``` to ```Stack[-0x68]:8```. Recreating the struct gives 3
char pointers ```char*``` with a length of 8 bytes each, and starting at an offset of 8, 16, 24. 

## Get the right passcode
We understand what the comapres are checking for, but what are the functions doing?
Testing in GDB: 
```
run $(python -c 'print("12345678 \x41\x41\x41\x41\x42\x42\x42\x42 \xfc\x43\x43\x43\x44\x44\x44\x44")')
``` 
The ```key value``` is XORed with the each single character in the ```username value``` and the last byte is stored in ```al``` of which ```0x13``` is subtracted from the result. The result of which is compared to the supplied password. 

E.g. for the first iteration of the while loop in ```gen_password```: ```12345678 (0xbc614e)``` is XORed with ```65 (0x41)```
```
  b    c    6    1    4   e
1011 1100 0110 0001 0100 1110
  0    0    0    0    4   1
0000 0000 0000 0000 0100 0001
xor result: 
  b    c    6    1    0    f
1011 1100 0110 0001 0000 1111
```
of which the last byte ```f``` is stored in the ```al``` register. ```0xf (15)``` minus ```0x13 (19)``` = ```-4```. 


