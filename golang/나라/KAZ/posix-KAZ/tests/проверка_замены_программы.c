/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <система/ожидание_потомков.h>
#include <unistd.h>

static void say(const char *text, unsigned int число_цифр)
{
    (void)писать(STDOUT_FILENO, text, число_цифр);
}

int main(void)
{
    int состояние;
    int дескриптор_файла;
    char *аргументы_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (ждать_указанного_потомка(-1, &состояние, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (ждать_потомка(&состояние) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    дескриптор_файла = открыть("/USER2", O_RDONLY);
    if (дескриптор_файла < 0 || дублировать_ссылку_под_заданным_номером(дескриптор_файла, 10) != 10 || управлять_файлом(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        немедленно_завершить(98);
    }
    if (дескриптор_файла != 10)
        (void)закрыть(дескриптор_файла);

    (void)заменить_исполняемую_программу("/PXEXEC", аргументы_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    немедленно_завершить(99);
}
