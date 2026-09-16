/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <النظام/انتظار_العمليات_الفرعية.h>
#include <unistd.h>

static void say(const char *text, unsigned int عدد_الخانات)
{
    (void)كتابة(STDOUT_FILENO, text, عدد_الخانات);
}

int main(void)
{
    int الحالة;
    int واصف_الملف;
    char *المعاملات_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (انتظار_العملية_الفرعية_المحددة(-1, &الحالة, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (انتظار_عملية_فرعية(&الحالة) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    واصف_الملف = فتح("/USER2", O_RDONLY);
    if (واصف_الملف < 0 || نسخ_مرجع_الملف_إلى_رقم_محدد(واصف_الملف, 10) != 10 || التحكم_في_الملف(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        إنهاء_فوري(98);
    }
    if (واصف_الملف != 10)
        (void)إغلاق(واصف_الملف);

    (void)استبدال_البرنامج_الجاري("/PXEXEC", المعاملات_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    إنهاء_فوري(99);
}
