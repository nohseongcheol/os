/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct stat st;
    struct utsname sistem_kimliği;
    int dosya_tanımlayıcısı = Aç("/USER1", O_RDONLY);
    int copy = dosya_tanımlayıcısı >= 0 ? dup(dosya_tanımlayıcısı) : -1;
    if (copy >= 0) Kapat(copy);
    if (dosya_tanımlayıcısı >= 0) {
        fstat(dosya_tanımlayıcısı, &st);
        lseek(dosya_tanımlayıcısı, 0, SEEK_SET);
        Kapat(dosya_tanımlayıcısı);
    }
    stat("/", &st);
    uname(&sistem_kimliği);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
