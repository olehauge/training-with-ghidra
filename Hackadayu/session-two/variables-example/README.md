# Variables
For this challenge we were to:
- Find the number of used global variables
- Find the number of used local variables
- Find the proper passcode

## Find the number of global variables
For this lecture we learned that the global variables of a C program is stored in the ```.data``` section of the file. 
With this knowledge we can look at the assembly code and search for non-local variables that are used, and by cross referencing them with the data in the ```.data``` part
we can see that the following are the global variables used. 

Global variables in main:
```
                     LAB_0010075b                                    XREF[1]:     001007c3(j)  
0010075b 48 8b 15        MOV        RDX,qword ptr [XorMe]                            = DEADBEEFFACECAFEh
         ae 08 20 00
...      
00100773 48 8b 15        MOV        RDX,qword ptr [globalVar]                        = 00100868
         9e 08 20 00
```
Cross referenced with the data in ```.data```:
```
                     __data_start                                    XREF[2]:     Entry Point(*), 
                     data_start                                                   _elfSectionHeaders::000005d0(*)  
00301000 00              ??         00h
00301001 00              ??         00h
00301002 00              ??         00h
00301003 00              ??         00h
00301004 00              ??         00h
00301005 00              ??         00h
00301006 00              ??         00h
00301007 00              ??         00h
                     __dso_handle                                    XREF[3]:     Entry Point(*), 
                                                                                  __do_global_dtors_aux:001006b7(R
                                                                                  00301008(*)  
00301008 08 10 30        addr       __dso_handle                                     = 00301008
         00 00 00 
         00 00
                     XorMe                                           XREF[2]:     Entry Point(*), main:0010075b(R)  
00301010 fe ca ce        undefined8 DEADBEEFFACECAFEh
         fa ef be 
         ad de
                     globalVar                                       XREF[2]:     Entry Point(*), main:00100773(R)  
00301018 68 08 10        addr       s_KeYpress_00100868                              = "KeYpress"
         00 00 00 
         00 00
```
We can also see (in Ghidra) that the global variables are highlighted with a pink color.

## Find the number of used local variables
The local variables are decalred within the function in question. In our case, this is the main function. At the begining of the function we can see that 
all the local variables are declared and by looking through the assembly code we can verify that they are indeed being used. 
```
                     **************************************************************
                     *                          FUNCTION                          *
                     **************************************************************
                     undefined main()
     undefined         AL:1           <RETURN>
     undefined8        Stack[-0x10]:8 local_10                                XREF[2]:     00100747(W), 
                                                                                           00100799(R)  
     undefined4        Stack[-0x14]:4 local_14                                XREF[7]:     0010074b(W), 
                                                                                           00100752(W), 
                                                                                           00100762(R), 
                                                                                           0010077a(R), 
                                                                                           00100793(R), 
                                                                                           001007bb(RW), 
                                                                                           001007bf(R)  
     undefined1        Stack[-0x15]:1 local_15                                XREF[2]:     00100790(W), 
                                                                                           001007a3(R)  
     undefined1        Stack[-0x16]:1 local_16                                XREF[2]:     00100770(W), 
                                                                                           00100787(R)  
     undefined4        Stack[-0x1c]:4 local_1c                                XREF[2]:     001006f2(W), 
                                                                                           001006f9(R)  
     undefined8        Stack[-0x28]:8 local_28                                XREF[3]:     001006f5(W), 
                                                                                           0010071a(R), 
                                                                                           0010073f(R)  
                     main                                            XREF[4]:     Entry Point(*), 
                                                                                  _start:001005fd(*), 0010093c, 
                                                                                  001009e8(*)  
001006ea 55              PUSH       RBP
001006eb 48 89 e5        MOV        RBP,RSP
001006ee 48 83 ec 20     SUB        RSP,0x20
...
```
We can also see this by expanding the main function in the Symbol Tree window as this will list out all the local variables in the function. 

## Find the proper passcode
- We see that the program takes a string as input. 
- The sting has to be longer than ```8``` characters. 
- A while loop loops through the user supplied string and fails if the characters does not match the compares done to the globaly stored string. 
    - The ```XorMe``` string, ```deadbeeffacecafe```, is used to get 2 and 2 characters (once iteration per loop cycle), which are derived by first left shifting the current pointer value 3 times, 
    before right shifting the string with that resulting value. These 2 characters are then stored in ```EAX```. **NOTE!** The characters are gotten in reversed order i.e. the first to char. are ```fe```.
    - The ```globalVar``` string, ```KeYpress```, is used to get one character (once iteration per loop cycle), thus iterating over the string and storing the current letter in ```EDX```.
    - ```EAX``` and ```EDX``` are added togheter and then ```1``` is added to that sum. 
    - The resulting value is stored in ```AL```, which means that we store the two last values i.e. for ```ce``` + ```K``` + ```1``` = ```14A``` we store ```4A``` which is the character ```J```. 
    - This value is compared to the corresponding character in the iteration of the user supplied string i.e. the first char. of the string has to be ```J```. 

This get a bit tricky as some of the values are non-readable ASCII characters like ```0x30``` == ```alt```. In order to pass such values to the program we can use
Python. 
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-two/exercises# ./variables-example $(python -c 'print("\x4a\x30\x28\x6b\x62\x24\x21\x52")')
Proper keycode supplied, well done!
```
This way the ```argv``` will get the values directly from the command line. **NOTE!** The program only need these eight first values to be correct. We can supply more characters after these eigth if we want to.
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-two/exercises# ./variables-example $(python -c 'print("\x4a\x30\x28\x6b\x62\x24\x21\x52\x41\x41\x41\x41")')
Proper keycode supplied, well done!
```

