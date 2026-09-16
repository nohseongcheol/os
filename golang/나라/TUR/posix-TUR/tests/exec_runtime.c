/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int rakam_sayısı)
{
    (void)Yazma(STDOUT_FILENO, text, rakam_sayısı);
}

int main(void)
{
    int durum;
    int dosya_tanımlayıcısı;
    char *bağımsız_değişkenler_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &durum, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&durum) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    dosya_tanımlayıcısı = Aç("/USER2", O_RDONLY);
    if (dosya_tanımlayıcısı < 0 || dup2(dosya_tanımlayıcısı, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (dosya_tanımlayıcısı != 10)
        (void)Kapat(dosya_tanımlayıcısı);

    (void)execve("/PXEXEC", bağımsız_değişkenler_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
