# Files
For this challenge we were to:
- What is the difference between this exercise and the struct and pointer exercises?
- What file operations are being performed?
- Find the password.

## Initial analysis
```
int open(char * __file, int __oflag, ...)

int               EAX:4          <RETURN>
char *            RDI:8          __file
int               ESI:4          __oflag
```
rsi set to 0x0
rdi set to string: `key.y`
eax set to 0x0 (cleared for the return value). The return value of open() is a file descriptor.

```
ssize_t read(int fd, void *buf, size_t count);

ssize_t           RAX:8          <RETURN>
int               EDI:4          __fd
void *            RSI:8          __buf
size_t            RDX:8          __nbytes
```
rsi set to `rcx` = `[RBP + -0x6c]`
rdi set to `eax` = `dword ptr [RBP + open_returnValue]`
edx set to `0x4`
rax: On success, the number of bytes read is returned.


## NOTES
Stores the value in `argc` into the memory location pointed to by `RBP + stored_argc`.
```
MOV        dword ptr [RBP + stored_argc],argc(rdi)
```
The lea instruction places the address specified by its first operand into the register specified by its second operand.
```
LEA        RCX,[RBP + -0x6c]
```
