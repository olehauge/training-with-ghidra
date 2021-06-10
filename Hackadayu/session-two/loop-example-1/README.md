# Loops and Iterations
For this challenge we were to:
- how many times does this loop run?
- what is this loop looking for?
- do the values used represent any thing?
- can you get access?

The syntax was improved by modifying the function signature to ```int main (int argc, char **argv)```.

## Number of runs
Looking at the assembly code we can see that the lenght of the string is stored in a variable. If this equals ``15`` the loop will start and run for 15 turns.
```
                     firstLoopCheck                                  XREF[1]:     001006fc(j)  
0010073a 8b 45 f4        MOV        EAX,dword ptr [RBP + counter]
0010073d 3b 45 fc        CMP        EAX,dword ptr [RBP + stringLength]
00100740 7c bc           JL         firstLoop
```

## What is it looking for
The loop is looking for two values, ``0x40`` and ``0x5a``:
```
0010070e 48 01 d0        ADD        RAX,RDX
00100711 0f b6 00        MOVZX      EAX,byte ptr [RAX]
00100714 3c 40           CMP        AL,0x40
00100716 7e 1e           JLE        incrementValue
...
0010072e 3c 5a           CMP        AL,0x5a
00100730 7f 04           JG         incrementValue
00100732 83 45 f8 01     ADD        dword ptr [RBP + matches],0x1
```
If both are valid the value stored at ```RBP + matches``` will be incremented by one. The values can also be represented by ``@`` and ``Z``.

## Getting access
To get access we also have to consider the following addition which happens before each of the compares in the loop:
```
                     firstLoop                                       XREF[1]:     00100740(j)  
001006fe 48 8b 45 e0     MOV        RAX,qword ptr [RBP + local_28]
00100702 48 83 c0 08     ADD        RAX,0x8
00100706 48 8b 10        MOV        RDX,qword ptr [RAX]
00100709 8b 45 f4        MOV        EAX,dword ptr [RBP + counter]
0010070c 48 98           CDQE
0010070e 48 01 d0        ADD        RAX,RDX
00100711 0f b6 00        MOVZX      EAX,byte ptr [RAX]
```
We can see that the value of ``8`` is added to the values of the letter in the string which is being copmared. 
The compare after the while loop checking if the ``mathces`` value equals 8 has to be passed as well. This means that we need to pass the check in the while loop exactly ``8`` times. 
```
00100742 83 7d f8 08     CMP        dword ptr [RBP + matches],8
00100746 74 0e           JZ         cmpThreeOK_SUCCESS
```
This means that we have to use ASCII characters that have a value greater than ``0x40`` but less than ``0x5a`` after the addition of ``8``. 

Running the program with the following string of ASCI characters grants us access: ``/0x41/0x42/0x43/0x44/0x45/0x46/0x47/0x48/0x69/0x6A/0x6B/0x6C/0x6D/0x6E/0x6F``, as the length of the string is ``15`` and the first ``8`` characters are greater than 64 and less than 90 after the addtion of ``8``. 
````
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-two/exercises# ./loop-example-1 ABCDEFGHijklmno
Congratulations, access granted!
