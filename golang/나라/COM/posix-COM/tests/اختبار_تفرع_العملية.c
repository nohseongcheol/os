/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <النظام/انتظار_العمليات_الفرعية.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int عدد_الخانات)
{
    (void)كتابة(STDOUT_FILENO, text, عدد_الخانات);
}

int main(void)
{
    int الحالة;
    pid_t parent = جلب_معرف_العملية();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int واصف_الملف;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = إنشاء_عملية_فرعية();
    if (child == 0) {
        private_value = 20;
        if (جلب_معرف_العملية_الأم() != parent || private_value != 20)
            إنهاء_فوري(90);
        إنهاء_فوري(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        إنهاء_فوري(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = انتظار_العملية_الفرعية_المحددة(child, &الحالة, 0);
    if (waited == child && WIFEXITED(الحالة) && WEXITSTATUS(الحالة) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        إنهاء_فوري(1);
    }

    child = إنشاء_عملية_فرعية();
    if (child == 0)
        إنهاء_فوري(29);
    waited = انتظار_عملية_فرعية(&الحالة);
    if (waited == child && WIFEXITED(الحالة) && WEXITSTATUS(الحالة) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        إنهاء_فوري(1);
    }

    واصف_الملف = فتح("/USER2", O_RDONLY);
    child = إنشاء_عملية_فرعية();
    if (child == 0) {
        (void)إغلاق(واصف_الملف);
        إنهاء_فوري(0);
    }
    waited = انتظار_العملية_الفرعية_المحددة(child, &الحالة, 0);
    if (واصف_الملف >= 0 && waited == child && قراءة(واصف_الملف, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        إنهاء_فوري(1);
    }
    (void)إغلاق(واصف_الملف);

    for (iteration = 0; iteration < 2; iteration++) {
        child = إنشاء_عملية_فرعية();
        if (child == 0)
            إنهاء_فوري(iteration);
        if (child < 0 || انتظار_العملية_الفرعية_المحددة(child, &الحالة, 0) != child ||
            !WIFEXITED(الحالة) || WEXITSTATUS(الحالة) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            إنهاء_فوري(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    إنهاء_فوري(0);
}
