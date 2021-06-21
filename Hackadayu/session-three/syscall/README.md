# System calls
For this challenge we were to:
- Find how many system calls that were performed
- Find out what the system calls do
- Figure out what the program does without running it
- Find the entry point of the program

# Initial analysis of the program
First, the value that dictates what syscall is called is stored in the `rax` register. Arguments are passed and returned as with functions. 

There are 4 syscalls in the program:
1. The first syscall:
   - `eax`: set to `0x2`
   - `rdi`: set to `fileName` = `"syscalls.txt"`
   - `rsi`: set to `fileFlags` = `0000000000000042`
   - `rdx`: set to `fileMode` = `0000000000000180`

This means that the first syscall is `open(const char *pathname, int flags, mode_t mode)`, where `rdi` sets the path to the value stored at `fileName`, `rdx` 
sets the mode to the value stored at `fileMode`, and `rsi` sets the flag to the value stored at `fileFlag`. 

2. The second syscall:
   - `eax`: set to `0x1`
   - `rdi`: set to `fileDescriptor` = value at `rax`
   - `rsi`: set to `msg` = starts at `68h` and should print out `"hello-hackaday"`
   - `edx`: set to `0xe`
   
This means that the first syscall is `write(int fildes, const void *buf, size_t nbytes);`, 
