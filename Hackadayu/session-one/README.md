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
The program still checks for the user supplied password before testing for the password length greater than 4. We see that the ```rdi``` register is used by ```strlen``` and that the result of the function is stored in the ```rax``` register.
````
004005a3 48 8b 45 f0     MOV        RAX,qword ptr [RBP + local_18]
004005a7 48 83 c0 08     ADD        RAX,0x8
004005ab 48 8b 00        MOV        RAX,qword ptr [RAX]
004005ae 48 89 c7        MOV        RDI,RAX
004005b1 e8 aa fe        CALL       strlen                                           size_t strlen(char * __s)
         ff ff
004005b6 48 83 f8 04     CMP        RAX,0x4
004005ba 77 11           JA         LAB_004005cd

````
Next we see that the supplied password is stored in the ```rax``` register before storing the first 32 bits in the ```eax```register. We then see that the comparing is done using the ```AL``` register, which is the first 8 bits of the ```AX``` register. This means that we are essentially looking at the first letter of the supplied password, albeit represented in hex. As we can see the compare is valid if our ```AL``` register conatins 0x68 == 'h'. 
````
                     LAB_004005cd                                    XREF[1]:     004005ba(j)  
004005cd 48 8b 45 f0     MOV        RAX,qword ptr [RBP + local_18]
004005d1 48 83 c0 08     ADD        RAX,0x8
004005d5 48 8b 00        MOV        RAX,qword ptr [RAX]
004005d8 0f b6 00        MOVZX      EAX,byte ptr [RAX]
004005db 3c 68           CMP        AL,0x68
004005dd 75 27           JNZ        LAB_00400606
...
````
Further we have a new compare against the suplied password. This time we can move the address by 4 ```ADD   RAX,0x4```, which means that we focus on the 5th letter of the password. It has to be equivalent of 0x75 == 'u'.
````
...
004005df 48 8b 45 f0     MOV        RAX,qword ptr [RBP + local_18]
004005e3 48 83 c0 08     ADD        RAX,0x8
004005e7 48 8b 00        MOV        RAX,qword ptr [RAX]
004005ea 48 83 c0 04     ADD        RAX,0x4
004005ee 0f b6 00        MOVZX      EAX,byte ptr [RAX]
004005f1 3c 75           CMP        AL,0x75
004005f3 75 11           JNZ        LAB_00400606
004005f5 bf f0 06        MOV        EDI=>s_Correct_--_maybe_we_should_pay_a_004006   = "Correct -- maybe we should pa
         40 00
004005fa e8 51 fe        CALL       puts                                             int puts(char * __s)
         ff ff
...
````
This gives that any password longer than 4 characters starting with 'h' and having 'u' as the fifth character will be accepted. Running the program in the docker environment shows that the password can be ```h---u```.
````
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-one/exercises# ./c2 h---u
Correct -- maybe we should pay attention to more characters...
````
# Challenge three
some text

# Challenge four
some text
