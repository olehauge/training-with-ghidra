# System calls
For this challenge we were to:
- Find how many system calls that were performed
- Find out what the system calls do
- Figure out what the program does without running it
- Find the entry point of the program
 
## General information
### Register mapping for system call invocation using syscall
| system call number | 1st parameter      | 2nd parameter      | 3rd parameter      | 4th parameter      | 5th parameter      | 6th parameter      | result             |
|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|
| rax	               | rdi	               | rsi	               | rdx	               | r10	               | r8	               | r9	               | rax                | 

### Syscall values (relevant)
| rax           | Name          | Entry point   | Documentation |
|:-------------:|:-------------:|:-------------:|:-------------:|
| 0	          | read	        | sys_read      | [read(2)](https://man7.org/linux/man-pages/man2/read.2.html)          |
| 1 	          | write |	sys_write | [write(2)](https://man7.org/linux/man-pages/man2/write.2.html)          |
| 2		       | open	| sys_open | [open(2)](https://man7.org/linux/man-pages/man2/open.2.html)          |
| 3		       | close |sys_close | [close(2)](https://man7.org/linux/man-pages/man2/close.2.html)          |

## Initial analysis of the program
First, the value that dictates what syscall is called is stored in the `rax` register. Arguments are passed and returned as with functions. 

There are 4 syscalls in the program:
1. The first syscall (open):
   - `eax`: set to `0x2`
   - `rdi`: set to `fileName` = `"syscalls.txt"`
   - `rsi`: set to `fileFlags` = `0000000000000042`
   - `rdx`: set to `fileMode` = `0000000000000180`

This means that the first syscall is `open(const char *pathname, int flags, mode_t mode)`, where `rdi` sets the `pathname` to the value stored at `fileName`, `rsi` sets `flags` to the value stored at `fileFlag`, and `rdx` sets `mode` to the value stored at `fileMode`. The `open()` system call opens the file specified by `pathname`.  If the specified file does not exist, it may optionally (if O_CREAT is specified in flags) be created by `open()`. The return value of `open()` is a file descriptor, a small, nonnegative integer that is an index to an entry in the process's table of open file descriptors. 

2. The second syscall (write):
   - `eax`: set to `0x1`
   - `rdi`: set to `fileDescriptor` = value at `rax`
   - `rsi`: set to `msg` = starts at `68h` and should print out `"hello-hackaday"`
   - `edx`: set to `0xe`
   
This means that the first syscall is `write(int fd, const void *buf, size_t count);`, where `rdi` sets the `fd` to ?, `rsi` sets `buf` to the start point for the write function, `edx` sets the `count`. Write() writes up to `count` bytes from the buffer starting at `buf` to the file referred to by the file descriptor `fd`.
