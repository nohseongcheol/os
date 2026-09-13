#include <errno.h>
#include <fcntl.h>
#include <அமைப்பு/stat.h>
#include <அமைப்பு/அமைப்பு_அடையாளம்.h>
#include <அமைப்பு/சேய்_காத்திருப்பு.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int நீளம் = 0;
    while (text[நீளம்] != 0)
        நீளம்++;
    return நீளம்;
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
    (void)எழுது(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *அமைப்பின்_அடையாளம், int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(அமைப்பின்_அடையாளம்);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *நிலை)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = குறித்த_சேய்க்குக்_காத்திரு(child, நிலை, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", செயல்முறை_அடையாளத்தைப்_பெறு() > 0);
    report("getppid", தாய்_செயல்முறை_அடையாளத்தைப்_பெறு() >= 0);
    report("getuid", பயனர்_அடையாளத்தைப்_பெறு() == 0);
    report("geteuid", நடப்பு_உரிமைப்_பயனர்_அடையாளத்தைப்_பெறு() == 0);
    report("getgid", குழு_அடையாளத்தைப்_பெறு() == 0);
    report("getegid", நடப்பு_உரிமைக்_குழு_அடையாளத்தைப்_பெறு() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct கோப்பு_நிலை st;

    report("getcwd", பணி_அடைவின்_பாதையைப்_பெறு(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", பணி_அடைவின்_பாதையைப்_பெறு(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", பணி_அடைவின்_பாதையைப்_பெறு((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", பணி_அடைவை_மாற்று("/") == 0);
    report("chdir-dot", பணி_அடைவை_மாற்று(".") == 0);
    report("chdir-root-dot", பணி_அடைவை_மாற்று("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(பணி_அடைவை_மாற்று("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(பணி_அடைவை_மாற்று((const char *)0), EFAULT));

    report("access-file", அணுகல்_உரிமையைச்_சோதி("/USER2", F_OK) == 0 && அணுகல்_உரிமையைச்_சோதி("/USER2", R_OK) == 0);
    report("access-root", அணுகல்_உரிமையைச்_சோதி("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(அணுகல்_உரிமையைச்_சோதி("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(அணுகல்_உரிமையைச்_சோதி("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(அணுகல்_உரிமையைச்_சோதி("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(அணுகல்_உரிமையைச்_சோதி("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(அணுகல்_உரிமையைச்_சோதி((const char *)0, F_OK), EFAULT));

    report("stat-root", கோப்பு_நிலை("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", கோப்பு_நிலை("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", இணைப்பின்_சொந்த_நிலையைப்_பெறு("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(கோப்பு_நிலை("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(கோப்பு_நிலை((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(கோப்பு_நிலை("/", (struct கோப்பு_நிலை *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct கோப்பு_நிலை st;
    int கோப்பு_விவரிப்பி;
    int root;

    கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    report("open-readonly", கோப்பு_விவரிப்பி >= 3);
    if (கோப்பு_விவரிப்பி >= 0) {
        report("read-bytes", படி(கோப்பு_விவரிப்பி, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", கோப்பின்_படிப்பிடத்தை_நகர்த்து(கோப்பு_விவரிப்பி, 0, SEEK_SET) == 0);
        report("lseek-cur", கோப்பின்_படிப்பிடத்தை_நகர்த்து(கோப்பு_விவரிப்பி, 1, SEEK_CUR) == 1);
        report("lseek-end", கோப்பின்_படிப்பிடத்தை_நகர்த்து(கோப்பு_விவரிப்பி, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", கோப்பின்_படிப்பிடத்தை_நகர்த்து(கோப்பு_விவரிப்பி, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", கோப்பின்_படிப்பிடத்தை_நகர்த்து(கோப்பு_விவரிப்பி, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", திறந்த_கோப்பின்_நிலையைப்_பெறு(கோப்பு_விவரிப்பி, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(திறந்த_கோப்பின்_நிலையைப்_பெறு(கோப்பு_விவரிப்பி, (struct கோப்பு_நிலை *)0), EFAULT));
        report("fsync-file", கோப்பின்_பதிவை_ஒத்திசை(கோப்பு_விவரிப்பி) == 0);
        report("close-file", மூடு(கோப்பு_விவரிப்பி) == 0);
        errno = 0;
        report("closed-fd", failed_with(மூடு(கோப்பு_விவரிப்பி), EBADF));
    }

    root = திற("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", திறந்த_கோப்பின்_நிலையைப்_பெறு(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", படி(root, bytes, 1) == -1 && errno == EISDIR);
        (void)மூடு(root);
    }

    report("fstat-character", திறந்த_கோப்பின்_நிலையைப்_பெறு(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", எழுது(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", படி(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", படி(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", எழுது(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", கோப்பின்_படிப்பிடத்தை_நகர்த்து(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(கோப்பின்_பதிவை_ஒத்திசை(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(திற("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(திற((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(திற("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(திற("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(திற("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(திற("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(திற("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(திற("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(கோப்பை_உருவாக்கு("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(மூடு(-1), EBADF));

    அனைத்துப்_பதிவுகளையும்_ஒத்திசை();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct கோப்பு_நிலை st;
    int கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (கோப்பு_விவரிப்பி < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = திறந்த_கோப்பின்_குறிப்பை_நகலெடு(கோப்பு_விவரிப்பி);
    report("dup", copy >= 0 && copy != கோப்பு_விவரிப்பி);
    if (copy >= 0) {
        report("dup-shared-offset", படி(கோப்பு_விவரிப்பி, &first, 1) == 1 && படி(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", மூடு(கோப்பு_விவரிப்பி) == 0 && திறந்த_கோப்பின்_நிலையைப்_பெறு(copy, &st) == 0);
        கோப்பு_விவரிப்பி = copy;
    }

    target = குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(கோப்பு_விவரிப்பி, 20);
    report("dup2", target == 20 && திறந்த_கோப்பின்_நிலையைப்_பெறு(20, &st) == 0);
    report("dup2-same", குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(கோப்பு_விவரிப்பி, கோப்பு_விவரிப்பி) == கோப்பு_விவரிப்பி);
    if (target == 20)
        (void)மூடு(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(கோப்பு_விவரிப்பி, 99), EBADF));

    report("fcntl-getfd", கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_GETFD) == 0);
    report("fcntl-setfd", கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_SETFD, FD_CLOEXEC) == 0 &&
           கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_GETFD) == FD_CLOEXEC);
    high = கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", கோப்பைக்_கட்டுப்படுத்து(high, F_GETFD) == 0);
        (void)மூடு(high);
    }
    report("fcntl-getfl", (கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_SETFL, O_APPEND) == 0 &&
           (கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(கோப்பைக்_கட்டுப்படுத்து(கோப்பு_விவரிப்பி, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(கோப்பைக்_கட்டுப்படுத்து(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(திறந்த_கோப்பின்_குறிப்பை_நகலெடு(-1), EBADF));
    (void)மூடு(கோப்பு_விவரிப்பி);
}

static void test_terminal_and_uname(void)
{
    struct utsname அமைப்பின்_அடையாளம்;
    int கோப்பு_விவரிப்பி;

    report("isatty-stdin", முனையமா_எனச்_சோதி(STDIN_FILENO) == 1);
    report("isatty-stdout", முனையமா_எனச்_சோதி(STDOUT_FILENO) == 1);
    கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    if (கோப்பு_விவரிப்பி >= 0) {
        errno = 0;
        report("isatty-enotty", முனையமா_எனச்_சோதி(கோப்பு_விவரிப்பி) == 0 && errno == ENOTTY);
        (void)மூடு(கோப்பு_விவரிப்பி);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", முனையமா_எனச்_சோதி(-1) == 0 && errno == EBADF);

    report("uname", அமைப்புத்_தகவலைப்_பெறு(&அமைப்பின்_அடையாளம்) == 0 && அமைப்பின்_அடையாளம்.sysname[0] != 0 &&
           அமைப்பின்_அடையாளம்.nodename[0] != 0 && text_equal(அமைப்பின்_அடையாளம்.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(அமைப்புத்_தகவலைப்_பெறு((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)மாறும்_நினைவக_முடிவை_நகர்த்து(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)மாறும்_நினைவக_முடிவை_நகர்த்து(32);
    report("sbrk-grow", old == start && மாறும்_நினைவக_முடிவை_நகர்த்து(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", மாறும்_நினைவக_முடிவை_அமை((void *)start) == 0 && மாறும்_நினைவக_முடிவை_நகர்த்து(0) == (void *)start);
}

void posix_test_process(void)
{
    int நிலை = 0;
    int கோப்பு_விவரிப்பி;
    char byte;
    pid_t parent = செயல்முறை_அடையாளத்தைப்_பெறு();
    pid_t child = சேய்_செயல்முறையை_உருவாக்கு();
    pid_t waited;

    if (child == 0) {
        if (செயல்முறை_அடையாளத்தைப்_பெறு() == parent || தாய்_செயல்முறை_அடையாளத்தைப்_பெறு() != parent)
            உடனே_முடி(90);
        உடனே_முடி(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &நிலை);
        report("waitpid", waited == child && WIFEXITED(நிலை) && WEXITSTATUS(நிலை) == 23);
        errno = 0;
        report("waitpid-echild", குறித்த_சேய்க்குக்_காத்திரு(child, &நிலை, WNOHANG) == -1 && errno == ECHILD);
    }

    கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0) {
        (void)மூடு(கோப்பு_விவரிப்பி);
        உடனே_முடி(0);
    }
    if (child > 0 && reap_nohang(child, &நிலை) == child) {
        report("fork-fd-isolation", படி(கோப்பு_விவரிப்பி, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (கோப்பு_விவரிப்பி >= 0)
        (void)மூடு(கோப்பு_விவரிப்பி);

    errno = 0;
    report("execve-enoent", failed_with(இயங்கும்_நிரலை_மாற்று("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(இயங்கும்_நிரலை_மாற்று((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0) {
        (void)இயங்கும்_நிரலை_மாற்று("/PXEXEC", (char *const *)0, (char *const *)0);
        உடனே_முடி(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &நிலை);
        report("execve", waited == child && WIFEXITED(நிலை) && WEXITSTATUS(நிலை) == 37);
    }

    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0)
        உடனே_முடி(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)செயல்முறை_அடையாளத்தைப்_பெறு();
        waited = சேய்க்குக்_காத்திரு(&நிலை);
        report("wait", waited == child && WIFEXITED(நிலை) && WEXITSTATUS(நிலை) == 29);
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
    உடனே_முடி(failures == 0 ? 0 : 1);
}
