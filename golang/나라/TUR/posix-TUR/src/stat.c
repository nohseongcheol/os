/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *yol, struct stat *aktarım_ara_belleği)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)yol, (long)aktarım_ara_belleği, 0, 0, 0, 0));
}

int lstat(const char *yol, struct stat *aktarım_ara_belleği)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)yol, (long)aktarım_ara_belleği, 0, 0, 0, 0));
}

int fstat(int dosya_tanımlayıcısı, struct stat *aktarım_ara_belleği)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, dosya_tanımlayıcısı, (long)aktarım_ara_belleği, 0, 0, 0, 0));
}

int uname(struct utsname *sistem_kimliği)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)sistem_kimliği, 0, 0, 0, 0, 0));
}
