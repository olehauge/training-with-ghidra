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
The c2 ELF binary still checks for the user supplied password before testing for the password length greater than 4. We see that the ```rdi``` register is used by ```strlen``` and that the result of the function is stored in the ```rax``` register.
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
This c3 challenge proved a bit harder to read just using the assembly instructions provided in Ghidra. It does still check for the supplied password and the password length has to be longer than 4. The challenging part came with the use of pointers in the following assemly code. I therefor opted to use GDB in order to dynamically look at the registers as the program got executed.
````
                     LAB_001006e1                                    XREF[1]:     001006cc(j)  
001006e1 c6 45 fd 20     MOV        byte ptr [RBP + local_b],0x20
001006e5 48 8b 45 e0     MOV        RAX,qword ptr [RBP + local_28]
001006e9 48 83 c0 08     ADD        RAX,0x8
001006ed 48 8b 00        MOV        RAX,qword ptr [RAX]
001006f0 48 83 c0 02     ADD        RAX,0x2
001006f4 0f b6 00        MOVZX      EAX,byte ptr [RAX]
001006f7 88 45 fe        MOV        byte ptr [RBP + local_a],AL
001006fa 48 8b 45 e0     MOV        RAX,qword ptr [RBP + local_28]
001006fe 48 83 c0 08     ADD        RAX,0x8
00100702 48 8b 00        MOV        RAX,qword ptr [RAX]
00100705 48 83 c0 03     ADD        RAX,0x3
00100709 0f b6 00        MOVZX      EAX,byte ptr [RAX]
0010070c 88 45 ff        MOV        byte ptr [RBP + local_9],AL
0010070f 0f b6 55 fe     MOVZX      EDX,byte ptr [RBP + local_a]
00100713 0f b6 45 ff     MOVZX      EAX,byte ptr [RBP + local_9]
00100717 29 c2           SUB        EDX,EAX
00100719 0f b6 45 fd     MOVZX      EAX,byte ptr [RBP + local_b]
0010071d 39 c2           CMP        EDX,EAX
0010071f 75 13           JNZ        LAB_00100734
00100721 48 8d 3d        LEA        RDI,[s_Correct!_You_figured_it_out_..._l_00100   = "Correct! You figured it out .
         10 01 00 00
00100728 e8 23 fe        CALL       puts                                             int puts(char * __s)
         ff ff
...
````
What I learned was that the ```0x20``` value is stored at the ```RBP + local_b``` address. The user supplied password is then stored in RAX and moved to focus on the second letter in the password, which in turn is stored at the ```RBP + local_a``` address.  Then we focus on the third letter in the password and store that to the ```RBP + local_9``` address. The ```EDX``` register is then loaded with the value stored at ```RBP + local_a```, while the ```EAX``` register is loaded with the value stored at ```RBP + local_9```, before subtracting EAX from EDX. The result is stored in ```EDX``` and compared to the value ```0x20``` stored at the ```RBP + local_b``` address. 

Furthermore, I realized that not only are the characters stored in memory as HEX-values, but they are also represented in reverse order. Lets say we enter ```AABB``` it would not be sotred as ```41414242``` but ```42424141```. 

What this means is that for the password to be correct the 2 and 3 last letters has to give the sum ```0x20``` == ```32``` when the 2nd is subtracted from the third i.e. 'E' == ```0x45``` subtracted from 'e' == ```0x65``` as this results in ```0x20```. 

Running the program in the docker environment with the password ```--eE-``` proves this. 
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-one/exercises# ./c3 --eE-
Correct! You figured it out ... looks like we have to upgrade our security...
```

# Challenge four
The fourth ELF binary,  c4, was a bit more challenging in that it contained a lot more jumps back and forth between addresses. This time I used the 'Block flow' graph tool to get an overview of the code flow in the main function. The program checked for user input and the password had to be longer than 9 characters. We then encounter our first while loop. 
````
...
                      start_while_loop
 004005f5 89 45 f4        MOV        dword ptr [RBP + local_14],pwd_lenght
 004005f8 c7 45 f0        MOV        dword ptr [RBP + i],0x0
          00 00 00 00
 004005ff eb 48           JMP        while_i_less_than_pwd_length
                      if_something                                    XREF[1]:     0040064f(j)  
 00400601 8b 45 f0        MOV        pwd_lenght,dword ptr [RBP + i]
 00400604 48 63 d0        MOVSXD     RDX,pwd_lenght
 00400607 48 8b 45 f8     MOV        pwd_lenght,qword ptr [RBP + local_10]
 0040060b 48 01 d0        ADD        pwd_lenght,RDX
 0040060e 0f b6 00        MOVZX      pwd_lenght,byte ptr [pwd_lenght]=>s_hackaday-u   = "hackaday-u"
 00400611 0f be c0        MOVSX      pwd_lenght,pwd_lenght
 00400614 8d 48 02        LEA        ECX,[pwd_lenght + 0x2]
 00400617 48 8b 45 e0     MOV        pwd_lenght,qword ptr [RBP + local_28]
 0040061b 48 83 c0 08     ADD        pwd_lenght,0x8
 0040061f 48 8b 10        MOV        RDX,qword ptr [pwd_lenght]
 00400622 8b 45 f0        MOV        pwd_lenght,dword ptr [RBP + i]
 00400625 48 98           CDQE
 00400627 48 01 d0        ADD        pwd_lenght,RDX
 0040062a 0f b6 00        MOVZX      pwd_lenght,byte ptr [pwd_lenght]
 0040062d 0f be c0        MOVSX      pwd_lenght,pwd_lenght
 00400630 39 c1           CMP        ECX,pwd_lenght
 00400632 74 11           JZ         increment_i
                      print_wrong_pwd
 00400634 bf 63 07        MOV        EDI=>s_Wrong_Password!_00400763,s_Wrong_Passwo   = "Wrong Password!"
          40 00
 00400639 e8 12 fe        CALL       puts                                             int puts(char * __s)
          ff ff
                      call_exit
 0040063e b8 ff ff        MOV        pwd_lenght,0xffffffff
          ff ff
 00400643 eb 1b           JMP        exit_program
                      increment_i                                     XREF[1]:     00400632(j)  
 00400645 83 45 f0 01     ADD        dword ptr [RBP + i],0x1
                      while_i_less_than_pwd_length                    XREF[1]:     004005ff(j)  
 00400649 8b 45 f0        MOV        pwd_lenght,dword ptr [RBP + i]
 0040064c 3b 45 f4        CMP        pwd_lenght,dword ptr [RBP + local_14]
 0040064f 7c b0           JL         if_something
                      print_correct_pwd
 00400651 bf 78 07        MOV        EDI=>s_Correct!_You've_entered_the_righ_004007   = "Correct! You've entered the r
          40 00
 00400656 e8 f5 fd        CALL       puts                                             int puts(char * __s)
          ff ff
...
````
After reading the assembly instructions I was still a bit uncertain about what the while loop compared so I used GDB again to dynamically go through the program step by step. What I learnt was that the while loop iterates over the suplied password and compares it to the ```hackaday-u``` string, but instead of comparing the direct HEX-values of the string to the suplied password it adds ```0x2``` to each character/value first. This means that in order for our password to be correct we have to add 2 to all the HEX-vaules represnting the ```hackaday-u``` string. For example, 'h' == 0x65; 0x68 + 0x2 = 0x6a == 'j' and so on...

Running the program in the docker environment with the password ```jcemcfc{/w``` proves this.
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-one/exercises# ./c4 jcemcfc{/w
Correct! You've entered the right password ... you're getting better at this!
```
