#include <sys/wait.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int số_chữ_số)
{
    (void)Ghi(STDOUT_FILENO, text, số_chữ_số);
}

int main(void)
{
    int trạng_thái;
    pid_t parent = getpid();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int bộ_mô_tả_tệp;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = fork();
    if (child == 0) {
        private_value = 20;
        if (getppid() != parent || private_value != 20)
            _exit(90);
        _exit(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        _exit(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = waitpid(child, &trạng_thái, 0);
    if (waited == child && WIFEXITED(trạng_thái) && WEXITSTATUS(trạng_thái) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        _exit(1);
    }

    child = fork();
    if (child == 0)
        _exit(29);
    waited = wait(&trạng_thái);
    if (waited == child && WIFEXITED(trạng_thái) && WEXITSTATUS(trạng_thái) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        _exit(1);
    }

    bộ_mô_tả_tệp = Mở("/USER2", O_RDONLY);
    child = fork();
    if (child == 0) {
        (void)Đóng(bộ_mô_tả_tệp);
        _exit(0);
    }
    waited = waitpid(child, &trạng_thái, 0);
    if (bộ_mô_tả_tệp >= 0 && waited == child && Đọc(bộ_mô_tả_tệp, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        _exit(1);
    }
    (void)Đóng(bộ_mô_tả_tệp);

    for (iteration = 0; iteration < 2; iteration++) {
        child = fork();
        if (child == 0)
            _exit(iteration);
        if (child < 0 || waitpid(child, &trạng_thái, 0) != child ||
            !WIFEXITED(trạng_thái) || WEXITSTATUS(trạng_thái) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            _exit(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    _exit(0);
}
