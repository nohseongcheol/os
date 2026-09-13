#ifndef _include_அமைப்பு_syscall
#define _include_அமைப்பு_syscall

long __syscall6(long number, long a1, long a2, long a3,
                      long a4, long a5, long a6);
long __syscall_result(long result);

#endif
