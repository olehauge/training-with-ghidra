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
