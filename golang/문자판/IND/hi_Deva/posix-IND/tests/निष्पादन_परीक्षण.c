/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <प्रणाली/stat.h>
#include <प्रणाली/प्रणाली_पहचान.h>
#include <प्रणाली/संतान_प्रतीक्षा.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int लंबाई = 0;
    while (text[लंबाई] != 0)
        लंबाई++;
    return लंबाई;
}

static int text_equal(const char *left, const char *right)
{
    unsigned int i = 0;
    while (left[i] != 0 && right[i] != 0) {
        if (left[i] != right[i])
            return 0;
        i++;
    }
    return left[i] == right[i];
}

static void say(const char *text)
{
    (void)लिखना(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *प्रणाली_की_पहचान, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(प्रणाली_की_पहचान);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *स्थिति)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = नियत_संतान_की_प्रतीक्षा_करना(child, स्थिति, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", प्रक्रिया_पहचान_पाना() > 0);
    report("getppid", जनक_प्रक्रिया_पहचान_पाना() >= 0);
    report("getuid", उपयोगकर्ता_पहचान_पाना() == 0);
    report("geteuid", प्रभावी_उपयोगकर्ता_पहचान_पाना() == 0);
    report("getgid", समूह_पहचान_पाना() == 0);
    report("getegid", प्रभावी_समूह_पहचान_पाना() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct संचिका_स्थिति st;

    report("getcwd", कार्य_निर्देशिका_पथ_पाना(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", कार्य_निर्देशिका_पथ_पाना(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", कार्य_निर्देशिका_पथ_पाना((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", कार्य_निर्देशिका_बदलना("/") == 0);
    report("chdir-dot", कार्य_निर्देशिका_बदलना(".") == 0);
    report("chdir-root-dot", कार्य_निर्देशिका_बदलना("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(कार्य_निर्देशिका_बदलना("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(कार्य_निर्देशिका_बदलना((const char *)0), EFAULT));

    report("access-file", पहुँच_अनुमति_जाँचना("/USER2", F_OK) == 0 && पहुँच_अनुमति_जाँचना("/USER2", R_OK) == 0);
    report("access-root", पहुँच_अनुमति_जाँचना("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(पहुँच_अनुमति_जाँचना("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(पहुँच_अनुमति_जाँचना("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(पहुँच_अनुमति_जाँचना("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(पहुँच_अनुमति_जाँचना("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(पहुँच_अनुमति_जाँचना((const char *)0, F_OK), EFAULT));

    report("stat-root", संचिका_स्थिति("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", संचिका_स्थिति("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", कड़ी_की_अपनी_स्थिति_पाना("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(संचिका_स्थिति("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(संचिका_स्थिति((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(संचिका_स्थिति("/", (struct संचिका_स्थिति *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct संचिका_स्थिति st;
    int संचिका_विवरणक;
    int root;

    संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    report("open-readonly", संचिका_विवरणक >= 3);
    if (संचिका_विवरणक >= 0) {
        report("read-bytes", पढ़ना(संचिका_विवरणक, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, 0, SEEK_SET) == 0);
        report("lseek-cur", पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, 1, SEEK_CUR) == 1);
        report("lseek-end", पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", खुली_संचिका_स्थिति_पाना(संचिका_विवरणक, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(खुली_संचिका_स्थिति_पाना(संचिका_विवरणक, (struct संचिका_स्थिति *)0), EFAULT));
        report("fsync-file", संचिका_अभिलेख_समकालित_करना(संचिका_विवरणक) == 0);
        report("close-file", बंद_करना(संचिका_विवरणक) == 0);
        errno = 0;
        report("closed-fd", failed_with(बंद_करना(संचिका_विवरणक), EBADF));
    }

    root = खोलना("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", खुली_संचिका_स्थिति_पाना(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", पढ़ना(root, bytes, 1) == -1 && errno == EISDIR);
        (void)बंद_करना(root);
    }

    report("fstat-character", खुली_संचिका_स्थिति_पाना(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", लिखना(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", पढ़ना(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", पढ़ना(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", लिखना(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", पठन_लेखन_स्थिति_बदलना(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(संचिका_अभिलेख_समकालित_करना(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(खोलना("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(खोलना((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(खोलना("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(खोलना("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(खोलना("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(खोलना("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(खोलना("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(खोलना("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(संचिका_बनाना("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(बंद_करना(-1), EBADF));

    सभी_अभिलेख_समकालित_करना();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct संचिका_स्थिति st;
    int संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (संचिका_विवरणक < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना(संचिका_विवरणक);
    report("dup", copy >= 0 && copy != संचिका_विवरणक);
    if (copy >= 0) {
        report("dup-shared-offset", पढ़ना(संचिका_विवरणक, &first, 1) == 1 && पढ़ना(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", बंद_करना(संचिका_विवरणक) == 0 && खुली_संचिका_स्थिति_पाना(copy, &st) == 0);
        संचिका_विवरणक = copy;
    }

    target = नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(संचिका_विवरणक, 20);
    report("dup2", target == 20 && खुली_संचिका_स्थिति_पाना(20, &st) == 0);
    report("dup2-same", नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(संचिका_विवरणक, संचिका_विवरणक) == संचिका_विवरणक);
    if (target == 20)
        (void)बंद_करना(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(संचिका_विवरणक, 99), EBADF));

    report("fcntl-getfd", संचिका_नियंत्रित_करना(संचिका_विवरणक, F_GETFD) == 0);
    report("fcntl-setfd", संचिका_नियंत्रित_करना(संचिका_विवरणक, F_SETFD, FD_CLOEXEC) == 0 &&
           संचिका_नियंत्रित_करना(संचिका_विवरणक, F_GETFD) == FD_CLOEXEC);
    high = संचिका_नियंत्रित_करना(संचिका_विवरणक, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", संचिका_नियंत्रित_करना(high, F_GETFD) == 0);
        (void)बंद_करना(high);
    }
    report("fcntl-getfl", (संचिका_नियंत्रित_करना(संचिका_विवरणक, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", संचिका_नियंत्रित_करना(संचिका_विवरणक, F_SETFL, O_APPEND) == 0 &&
           (संचिका_नियंत्रित_करना(संचिका_विवरणक, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(संचिका_नियंत्रित_करना(संचिका_विवरणक, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(संचिका_नियंत्रित_करना(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना(-1), EBADF));
    (void)बंद_करना(संचिका_विवरणक);
}

static void test_terminal_and_uname(void)
{
    struct utsname प्रणाली_की_पहचान;
    int संचिका_विवरणक;

    report("isatty-stdin", अंतक_है_या_नहीं_जाँचना(STDIN_FILENO) == 1);
    report("isatty-stdout", अंतक_है_या_नहीं_जाँचना(STDOUT_FILENO) == 1);
    संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    if (संचिका_विवरणक >= 0) {
        errno = 0;
        report("isatty-enotty", अंतक_है_या_नहीं_जाँचना(संचिका_विवरणक) == 0 && errno == ENOTTY);
        (void)बंद_करना(संचिका_विवरणक);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", अंतक_है_या_नहीं_जाँचना(-1) == 0 && errno == EBADF);

    report("uname", प्रणाली_जानकारी_पाना(&प्रणाली_की_पहचान) == 0 && प्रणाली_की_पहचान.sysname[0] != 0 &&
           प्रणाली_की_पहचान.nodename[0] != 0 && text_equal(प्रणाली_की_पहचान.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(प्रणाली_जानकारी_पाना((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)गतिशील_स्मृति_अंत_बदलना(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)गतिशील_स्मृति_अंत_बदलना(32);
    report("sbrk-grow", old == start && गतिशील_स्मृति_अंत_बदलना(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", गतिशील_स्मृति_अंत_निर्धारित_करना((void *)start) == 0 && गतिशील_स्मृति_अंत_बदलना(0) == (void *)start);
}

void posix_test_process(void)
{
    int स्थिति = 0;
    int संचिका_विवरणक;
    char byte;
    pid_t parent = प्रक्रिया_पहचान_पाना();
    pid_t child = संतान_प्रक्रिया_बनाना();
    pid_t waited;

    if (child == 0) {
        if (प्रक्रिया_पहचान_पाना() == parent || जनक_प्रक्रिया_पहचान_पाना() != parent)
            तुरंत_समाप्त_करना(90);
        तुरंत_समाप्त_करना(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &स्थिति);
        report("waitpid", waited == child && WIFEXITED(स्थिति) && WEXITSTATUS(स्थिति) == 23);
        errno = 0;
        report("waitpid-echild", नियत_संतान_की_प्रतीक्षा_करना(child, &स्थिति, WNOHANG) == -1 && errno == ECHILD);
    }

    संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    child = संतान_प्रक्रिया_बनाना();
    if (child == 0) {
        (void)बंद_करना(संचिका_विवरणक);
        तुरंत_समाप्त_करना(0);
    }
    if (child > 0 && reap_nohang(child, &स्थिति) == child) {
        report("fork-fd-isolation", पढ़ना(संचिका_विवरणक, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (संचिका_विवरणक >= 0)
        (void)बंद_करना(संचिका_विवरणक);

    errno = 0;
    report("execve-enoent", failed_with(निष्पादन_सामग्री_बदलना("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(निष्पादन_सामग्री_बदलना((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = संतान_प्रक्रिया_बनाना();
    if (child == 0) {
        (void)निष्पादन_सामग्री_बदलना("/PXEXEC", (char *const *)0, (char *const *)0);
        तुरंत_समाप्त_करना(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &स्थिति);
        report("execve", waited == child && WIFEXITED(स्थिति) && WEXITSTATUS(स्थिति) == 37);
    }

    child = संतान_प्रक्रिया_बनाना();
    if (child == 0)
        तुरंत_समाप्त_करना(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)प्रक्रिया_पहचान_पाना();
        waited = संतान_की_प्रतीक्षा_करना(&स्थिति);
        report("wait", waited == child && WIFEXITED(स्थिति) && WEXITSTATUS(स्थिति) == 29);
    }
}

int main(void)
{
    int bss_zeroed = checks == 0 && failures == 0;
    checks = 0;
    failures = 0;
    say("\nPOSIX-CORE:START\n");
    report("bss-zero", bss_zeroed);
    test_identity();
    test_paths();
    test_open_and_io();
    test_dup_and_fcntl();
    test_terminal_and_uname();
    report("suite-completed", checks > 60);
    if (failures == 0)
        say("POSIX-CORE:PASS\n");
    else
        say("POSIX-CORE:FAIL\n");
    तुरंत_समाप्त_करना(failures == 0 ? 0 : 1);
}
