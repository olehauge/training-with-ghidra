# Heap memory
For this challenge we were to:
- Figure out how much memory was allocated via malloc.
- Explain how this program differs from the loop example.

## Figuring out how much memory was allocated via malloc
The program allocates memory on the heap by passing the string lenght to ```calloc(n, sizeof(int))``` in the ```RAX``` register. This creates the string lenght times 4 bytes
as the string length is stored as a 4 byte integer. 

## The difference between this and the loop example
The biggest difference is the use of memory allocation in this program. The loop example simply stores the value on the stack, while this program allocates memory on the heap.
There are other small differences like:
- The loop example checks for a string of 15 characters, where 8 has to be in the range of upper case letters.
- This program does not checks for a string length, but runs for the length of the supplied string, where 12 of the characters has to be in the range of upper case letters.
    - The resulting uppercase letters printed out.
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-two/exercises# ./heap-example-1 AdsBCDsdfEFGsHIJdKLasdfkj
The result is: ABCDEFGHIJKL
```
