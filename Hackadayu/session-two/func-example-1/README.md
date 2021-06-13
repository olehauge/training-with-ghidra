# Functions
For this challenge we were to:
- How many functions the autoanalysis discover?
- How many local variables are present in each function?
    - What are their values?
- Do any of these functions take arguments?
    - If so, what are the arguments?

## How many functions the autoanalysis discover?
From the Symbol Tree window we see that the autoanlysis discovers 27 functions. 

## How many local variables are present in each function?
Of the 27 functions, 4 have local variables: 
- ```_start``` has ```local_10``` which is a Quad Word with a length of 8. 
- ```getLowerCase``` has 5 local variables:
    - ```local_c```: Double Word with a length of 4. 
    - ```local_10```: Double Word with a length of 4. 
    - ```local_14```: Double Word with a length of 4. 
    - ```local_20```: Quad Word with a length of 8. 
    - ```local_28```: Quad Word with a length of 8. 
- ```getUpperCase``` has 5 local variables:
    - ```local_c```: Double Word with a length of 4. 
    - ```local_10```: Double Word with a length of 4. 
    - ```local_14```: Double Word with a length of 4. 
    - ```local_20```: Quad Word with a length of 8. 
    - ```local_28```: Quad Word with a length of 8. 
- ```main``` has 4 local variables: 
    - ```local_20```: Quad Word with a length of 8. 
    - ```local_28```: Quad Word with a length of 8. 
    - ```local_2c```: Double Word with a length of 4. 
    - ```local_38```: Quad Word with a length of 8. 

## Do any of these functions take arguments?
All of these functions take arguments:
- ```_start``` takes 3 arguments:
    - Argument 1: (RDI) pointer to main()
    - Argument 2: (RSI) argc, you can see how it was the first thing popped off the stack
    - Argument 3: (RDX) argv, the value of RSP right after argc was popped.
- ```getLowerCase``` takes the string as an argument. 
- ```getUpperCase``` takes the string as an argument. 
- ```main``` takes 2 arguments, ```int argc``` and ```char **argv```. 

## Passing the checks
The program takes a user supplied string and uses the ```getLowerCase``` and ```getUpperCase``` functions to compare the returned values. If they are equal then we pass the check. 
- The main function does not check the string lenght. 
- ```getLowerCase``` checks the string for values between ```0x60``` and ```0x7a``` and increments the return value.
- ```getUpperCase``` checks the string for values between ```0x40``` and ```0x5a``` and increments the return value.
Looking at the ASCII table we see that these are the ranges of upper and lower case charaters, as the function names implies. As non of these functions check for the string lenght,
all we need to do is pass the equal ammount of upper and lower case characters.
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-two/exercises# ./func-example-1 Aa
Passcode generator passed, good job!
```
