#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int số_chữ_số)
{
    (void)Ghi(STDOUT_FILENO, text, số_chữ_số);
}

int main(void)
{
    int trạng_thái;
    int bộ_mô_tả_tệp;
    char *đối_số_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &trạng_thái, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&trạng_thái) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    bộ_mô_tả_tệp = Mở("/USER2", O_RDONLY);
    if (bộ_mô_tả_tệp < 0 || dup2(bộ_mô_tả_tệp, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (bộ_mô_tả_tệp != 10)
        (void)Đóng(bộ_mô_tả_tệp);

    (void)execve("/PXEXEC", đối_số_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
