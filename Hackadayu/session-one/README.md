# Challenge one
The c1 ELF binary was opened with Ghidra. The listing view showed the assembly instructions, while the decompile window showed the estimated C-code equivalent. Focusing on the assembly, we can see that it first does a compare to see if the password was supplied when the program was ran. Either it tells us to supply the password or it jumps to the ```LAB_00100745``` label.
```
00100729 83 7d ec 02     CMP        dword ptr [RBP + local_1c],0x2
0010072d 74 16           JZ         LAB_00100745
0010072f 48 8d 3d        LEA        RDI,[s_Please_supply_the_password!_00100858]     = "Please supply the password!\r"
         22 01 00 00
```
Looking at the ```LAB_00100745``` label, we see that the string ```hackadayu``` is compared to the suplied password at memory location ```00100774```.
```
                  LAB_00100745                                    XREF[1]:     0010072d(j)  
00100745 48 8d 05        LEA        RAX,[s_hackadayu_00100875]                       = "hackadayu"
         29 01 00 00
0010074c 48 89 45 f8     MOV        qword ptr [RBP + local_10],RAX=>s_hackadayu_00   = "hackadayu"
...
0010075c 48 89 c2        MOV        RDX,RAX
0010075f 48 8b 45 e0     MOV        RAX,qword ptr [RBP + local_28]
00100763 48 83 c0 08     ADD        RAX,0x8
00100767 48 8b 00        MOV        RAX,qword ptr [RAX]
...
00100774 e8 47 fe        CALL       strncmp                                          int strncmp(char * __s1, char * 
         ff ff
00100779 85 c0           TEST       EAX,EAX
0010077b 74 26           JZ         LAB_001007a3

```
Looking at the ```LAB_001007a3``` we see that we will be given the success print out. 
```
                      LAB_001007a3                                    XREF[1]:     0010077b(j)  
...
 001007b1 48 8d 3d        LEA        RDI,[s_Correct!_The_password_was_%s_thi_001008   = "Correct! The password was %s 
          00 01 00 00
 001007b8 b8 00 00        MOV        EAX,0x0
          00 00
 001007bd e8 2e fe        CALL       printf                                           int printf(char * __format, ...)
          ff ff
...
```
Running the program in the docker environment shows that the password was indeed ```hackadayu```.
````
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-one/exercises# ./c1 hackadayu
Correct! The password was hackadayu this whole time!
````

# Challenge two
some text

# Challenge three
some text

# Challenge four
some text
