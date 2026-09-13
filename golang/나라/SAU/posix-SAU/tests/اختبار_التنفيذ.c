#include <errno.h>
#include <fcntl.h>
#include <النظام/stat.h>
#include <النظام/هوية_النظام.h>
#include <النظام/انتظار_العمليات_الفرعية.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int الطول = 0;
    while (text[الطول] != 0)
        الطول++;
    return الطول;
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
    (void)كتابة(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *هوية_النظام, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(هوية_النظام);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *الحالة)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = انتظار_العملية_الفرعية_المحددة(child, الحالة, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", جلب_معرف_العملية() > 0);
    report("getppid", جلب_معرف_العملية_الأم() >= 0);
    report("getuid", جلب_معرف_المستخدم() == 0);
    report("geteuid", جلب_معرف_المستخدم_الفعلي() == 0);
    report("getgid", جلب_معرف_المجموعة() == 0);
    report("getegid", جلب_معرف_المجموعة_الفعلي() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct حالة_الملف st;

    report("getcwd", جلب_مسار_دليل_العمل(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", جلب_مسار_دليل_العمل(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", جلب_مسار_دليل_العمل((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", تغيير_دليل_العمل("/") == 0);
    report("chdir-dot", تغيير_دليل_العمل(".") == 0);
    report("chdir-root-dot", تغيير_دليل_العمل("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(تغيير_دليل_العمل("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(تغيير_دليل_العمل((const char *)0), EFAULT));

    report("access-file", فحص_صلاحيات_الوصول("/USER2", F_OK) == 0 && فحص_صلاحيات_الوصول("/USER2", R_OK) == 0);
    report("access-root", فحص_صلاحيات_الوصول("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(فحص_صلاحيات_الوصول("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(فحص_صلاحيات_الوصول("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(فحص_صلاحيات_الوصول("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(فحص_صلاحيات_الوصول("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(فحص_صلاحيات_الوصول((const char *)0, F_OK), EFAULT));

    report("stat-root", حالة_الملف("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", حالة_الملف("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", جلب_حالة_الرابط_نفسه("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(حالة_الملف("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(حالة_الملف((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(حالة_الملف("/", (struct حالة_الملف *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct حالة_الملف st;
    int واصف_الملف;
    int root;

    واصف_الملف = فتح("/USER2", O_RDONLY);
    report("open-readonly", واصف_الملف >= 3);
    if (واصف_الملف >= 0) {
        report("read-bytes", قراءة(واصف_الملف, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", نقل_موضع_الملف(واصف_الملف, 0, SEEK_SET) == 0);
        report("lseek-cur", نقل_موضع_الملف(واصف_الملف, 1, SEEK_CUR) == 1);
        report("lseek-end", نقل_موضع_الملف(واصف_الملف, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", نقل_موضع_الملف(واصف_الملف, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", نقل_موضع_الملف(واصف_الملف, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", جلب_حالة_الملف_المفتوح(واصف_الملف, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(جلب_حالة_الملف_المفتوح(واصف_الملف, (struct حالة_الملف *)0), EFAULT));
        report("fsync-file", مزامنة_بيانات_الملف(واصف_الملف) == 0);
        report("close-file", إغلاق(واصف_الملف) == 0);
        errno = 0;
        report("closed-fd", failed_with(إغلاق(واصف_الملف), EBADF));
    }

    root = فتح("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", جلب_حالة_الملف_المفتوح(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", قراءة(root, bytes, 1) == -1 && errno == EISDIR);
        (void)إغلاق(root);
    }

    report("fstat-character", جلب_حالة_الملف_المفتوح(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", كتابة(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", قراءة(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", قراءة(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", كتابة(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", نقل_موضع_الملف(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(مزامنة_بيانات_الملف(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(فتح("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(فتح((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(فتح("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(فتح("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(فتح("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(فتح("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(فتح("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(فتح("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(إنشاء_ملف("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(إغلاق(-1), EBADF));

    مزامنة_جميع_البيانات();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct حالة_الملف st;
    int واصف_الملف = فتح("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (واصف_الملف < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = نسخ_مرجع_الملف_المفتوح(واصف_الملف);
    report("dup", copy >= 0 && copy != واصف_الملف);
    if (copy >= 0) {
        report("dup-shared-offset", قراءة(واصف_الملف, &first, 1) == 1 && قراءة(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", إغلاق(واصف_الملف) == 0 && جلب_حالة_الملف_المفتوح(copy, &st) == 0);
        واصف_الملف = copy;
    }

    target = نسخ_مرجع_الملف_إلى_رقم_محدد(واصف_الملف, 20);
    report("dup2", target == 20 && جلب_حالة_الملف_المفتوح(20, &st) == 0);
    report("dup2-same", نسخ_مرجع_الملف_إلى_رقم_محدد(واصف_الملف, واصف_الملف) == واصف_الملف);
    if (target == 20)
        (void)إغلاق(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(نسخ_مرجع_الملف_إلى_رقم_محدد(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(نسخ_مرجع_الملف_إلى_رقم_محدد(واصف_الملف, 99), EBADF));

    report("fcntl-getfd", التحكم_في_الملف(واصف_الملف, F_GETFD) == 0);
    report("fcntl-setfd", التحكم_في_الملف(واصف_الملف, F_SETFD, FD_CLOEXEC) == 0 &&
           التحكم_في_الملف(واصف_الملف, F_GETFD) == FD_CLOEXEC);
    high = التحكم_في_الملف(واصف_الملف, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", التحكم_في_الملف(high, F_GETFD) == 0);
        (void)إغلاق(high);
    }
    report("fcntl-getfl", (التحكم_في_الملف(واصف_الملف, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", التحكم_في_الملف(واصف_الملف, F_SETFL, O_APPEND) == 0 &&
           (التحكم_في_الملف(واصف_الملف, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(التحكم_في_الملف(واصف_الملف, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(التحكم_في_الملف(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(نسخ_مرجع_الملف_المفتوح(-1), EBADF));
    (void)إغلاق(واصف_الملف);
}

static void test_terminal_and_uname(void)
{
    struct utsname هوية_النظام;
    int واصف_الملف;

    report("isatty-stdin", فحص_كون_الوصف_طرفية(STDIN_FILENO) == 1);
    report("isatty-stdout", فحص_كون_الوصف_طرفية(STDOUT_FILENO) == 1);
    واصف_الملف = فتح("/USER2", O_RDONLY);
    if (واصف_الملف >= 0) {
        errno = 0;
        report("isatty-enotty", فحص_كون_الوصف_طرفية(واصف_الملف) == 0 && errno == ENOTTY);
        (void)إغلاق(واصف_الملف);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", فحص_كون_الوصف_طرفية(-1) == 0 && errno == EBADF);

    report("uname", جلب_معلومات_النظام(&هوية_النظام) == 0 && هوية_النظام.sysname[0] != 0 &&
           هوية_النظام.nodename[0] != 0 && text_equal(هوية_النظام.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(جلب_معلومات_النظام((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)نقل_نهاية_الذاكرة_المتغيرة(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)نقل_نهاية_الذاكرة_المتغيرة(32);
    report("sbrk-grow", old == start && نقل_نهاية_الذاكرة_المتغيرة(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", تعيين_نهاية_الذاكرة_المتغيرة((void *)start) == 0 && نقل_نهاية_الذاكرة_المتغيرة(0) == (void *)start);
}

void posix_test_process(void)
{
    int الحالة = 0;
    int واصف_الملف;
    char byte;
    pid_t parent = جلب_معرف_العملية();
    pid_t child = إنشاء_عملية_فرعية();
    pid_t waited;

    if (child == 0) {
        if (جلب_معرف_العملية() == parent || جلب_معرف_العملية_الأم() != parent)
            إنهاء_فوري(90);
        إنهاء_فوري(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &الحالة);
        report("waitpid", waited == child && WIFEXITED(الحالة) && WEXITSTATUS(الحالة) == 23);
        errno = 0;
        report("waitpid-echild", انتظار_العملية_الفرعية_المحددة(child, &الحالة, WNOHANG) == -1 && errno == ECHILD);
    }

    واصف_الملف = فتح("/USER2", O_RDONLY);
    child = إنشاء_عملية_فرعية();
    if (child == 0) {
        (void)إغلاق(واصف_الملف);
        إنهاء_فوري(0);
    }
    if (child > 0 && reap_nohang(child, &الحالة) == child) {
        report("fork-fd-isolation", قراءة(واصف_الملف, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (واصف_الملف >= 0)
        (void)إغلاق(واصف_الملف);

    errno = 0;
    report("execve-enoent", failed_with(استبدال_البرنامج_الجاري("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(استبدال_البرنامج_الجاري((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = إنشاء_عملية_فرعية();
    if (child == 0) {
        (void)استبدال_البرنامج_الجاري("/PXEXEC", (char *const *)0, (char *const *)0);
        إنهاء_فوري(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &الحالة);
        report("execve", waited == child && WIFEXITED(الحالة) && WEXITSTATUS(الحالة) == 37);
    }

    child = إنشاء_عملية_فرعية();
    if (child == 0)
        إنهاء_فوري(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)جلب_معرف_العملية();
        waited = انتظار_عملية_فرعية(&الحالة);
        report("wait", waited == child && WIFEXITED(الحالة) && WEXITSTATUS(الحالة) == 29);
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
    إنهاء_فوري(failures == 0 ? 0 : 1);
}
