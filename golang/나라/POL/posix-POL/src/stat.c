/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *ścieżka, struct stat *bufor_przesyłania)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)ścieżka, (long)bufor_przesyłania, 0, 0, 0, 0));
}

int lstat(const char *ścieżka, struct stat *bufor_przesyłania)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)ścieżka, (long)bufor_przesyłania, 0, 0, 0, 0));
}

int fstat(int deskryptor_pliku, struct stat *bufor_przesyłania)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, deskryptor_pliku, (long)bufor_przesyłania, 0, 0, 0, 0));
}

int uname(struct utsname *tożsamość_systemu)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)tożsamość_systemu, 0, 0, 0, 0, 0));
}
