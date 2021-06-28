# Files
For this challenge we were to:
- What is the difference between this exercise and the struct and pointer exercises?
- What file operations are being performed?
- Find the password.

## Initial analysis
I expect the the program to open, read and use the data stored in files to create a password template (using XOR operations) and compare it to the supplied values. 
- The program looks for 3 files: `key.y`, `uname.x`, and `pword.z` which have contain a set minimum of values. 
- These values are then used by the program.
- The program will fail if these files does not exist, if they are empty, and if the supplied values are wrong. 

### Open and read
First for the `key.y` file:
```
int open(char * __file, int __oflag, ...)

int               EAX:4          <RETURN>
char *            RDI:8          __file
int               ESI:4          __oflag
```
- rsi set to 0x0
- rdi set to string: `key.y`
- eax set to 0x0 (cleared for the return value). The return value of open() is a file descriptor.

```
ssize_t read(int fd, void *buf, size_t count);

ssize_t           RAX:8          <RETURN>
int               EDI:4          __fd
void *            RSI:8          __buf
size_t            RDX:8          __nbytes
```
- rsi set to `rcx` = `[RBP + -0x6c]`
- rdi set to `eax` = `dword ptr [RBP + open_returnValue]`
- edx set to `0x4`
- rax: On success, the number of bytes read is returned.

Second for the `uname.x` file:
```
int open(char * __file, int __oflag, ...)

int               EAX:4          <RETURN>
char *            RDI:8          __file
int               ESI:4          __oflag
```
- rsi set to 0x0
- rdi set to string: `uname.x`
- eax set to 0x0 (cleared for the return value). The return value of open() is a file descriptor.

```
ssize_t read(int fd, void *buf, size_t count);

ssize_t           RAX:8          <RETURN>
int               EDI:4          __fd
void *            RSI:8          __buf
size_t            RDX:8          __nbytes
```
- rsi set to `rcx` = `qword ptr [RBP + heapAddress]`
- rdi set to `eax` = `dword ptr [RBP + open2_returnValue]`
- edx set to `0x255`
- rax: On success, the number of bytes read is returned.

Third for the `pword.z` file:
```
int open(char * __file, int __oflag, ...)

int               EAX:4          <RETURN>
char *            RDI:8          __file
int               ESI:4          __oflag
```
- rsi set to 0x0
- rdi set to string: `pword.z`
- eax set to 0x0 (cleared for the return value). The return value of open() is a file descriptor.

```
ssize_t read(int fd, void *buf, size_t count);

ssize_t           RAX:8          <RETURN>
int               EDI:4          __fd
void *            RSI:8          __buf
size_t            RDX:8          __nbytes
```
- rsi set to `rcx` = `qword ptr [RBP + heapAddress2]`
- rdi set to `eax` = `dword ptr [RBP + open3_returnValue]`
- edx set to `0x255`
- rax: On success, the number of bytes read is returned.

## Testing the program
Testing the program confirms my hypothesis.
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./files 
Could not find key file, please try again!

root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# touch key.y
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./files 
Not enough values in keyfile, please try again!

root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# echo "123" > key.y 
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./files 
Could not find username file, please try again!

root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# touch uname.x
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# echo "AAAABBBB" > uname.x 
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./files 
Could not find password file, please try again!

root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# touch pword.z 
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# echo "CCCCDDDD" > pword.z 
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./files 
Invalid character in password detected, exiting now!
```
What remains know is to reverse the `gen_password` function in order to supply the correct values in the files.

While testing I found that the `strlen` function stated that the files was one too long compared to the ASCII characters I had supplied. 
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# touch uname.x
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# wc -c uname.x 
9 uname.x
```
Doing some googling revealed that the `touch` command automatically supplied a trailing newline which was interpreted as a character. To avoid this i used `echo -n "sometext" > file.ending` to write values to the files without any trailing charaters. 
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# echo -n "AAAABBBB" > uname.x  
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# wc -c uname.x 
8 uname.x
```

## Finding the password
I reversed the `gen_password` function in Python and gave it the `key` and `username` parameters: `1234` and `AAAABBBB`, which resulted in the password: `\xe7\xe7\xe7\xe7\xe8\xe8\xe8\xe8`.

To get the success string from the program these values had to be in the files. I used Pyhton to get the non-printable ASCII-characters in the password file:
```
python -c 'print("\xe7\xe7\xe7\xe7\xe8\xe8\xe8\xe8")' > pword.z 
```

Running the program with these values yielded the following result:
```
root@faa7f12d4c35:/home/hackaday/hackaday-u/session-three/exercises# ./files 
Correct! Access granted!
```

## NOTES
Stores the value in `argc` into the memory location pointed to by `RBP + stored_argc`.
```
MOV        dword ptr [RBP + stored_argc],argc(rdi)
```
The lea instruction places the address specified by its first operand into the register specified by its second operand.
```
LEA        RCX,[RBP + -0x6c]
```
