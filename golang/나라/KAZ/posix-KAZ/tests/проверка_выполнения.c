#include <errno.h>
#include <fcntl.h>
#include <система/stat.h>
#include <система/сведения_о_системе.h>
#include <система/ожидание_потомков.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int длина = 0;
    while (text[длина] != 0)
        длина++;
    return длина;
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
    (void)писать(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *сведения_о_системе, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(сведения_о_системе);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *состояние)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = ждать_указанного_потомка(child, состояние, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", получить_номер_процесса() > 0);
    report("getppid", получить_номер_родительского_процесса() >= 0);
    report("getuid", получить_номер_пользователя() == 0);
    report("geteuid", получить_действующий_номер_пользователя() == 0);
    report("getgid", получить_номер_группы() == 0);
    report("getegid", получить_действующий_номер_группы() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct состояние_файла st;

    report("getcwd", получить_путь_рабочего_каталога(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", получить_путь_рабочего_каталога(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", получить_путь_рабочего_каталога((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", сменить_рабочий_каталог("/") == 0);
    report("chdir-dot", сменить_рабочий_каталог(".") == 0);
    report("chdir-root-dot", сменить_рабочий_каталог("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(сменить_рабочий_каталог("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(сменить_рабочий_каталог((const char *)0), EFAULT));

    report("access-file", проверить_права_доступа("/USER2", F_OK) == 0 && проверить_права_доступа("/USER2", R_OK) == 0);
    report("access-root", проверить_права_доступа("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(проверить_права_доступа("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(проверить_права_доступа("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(проверить_права_доступа("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(проверить_права_доступа("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(проверить_права_доступа((const char *)0, F_OK), EFAULT));

    report("stat-root", состояние_файла("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", состояние_файла("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", получить_состояние_самой_ссылки("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(состояние_файла("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(состояние_файла((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(состояние_файла("/", (struct состояние_файла *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct состояние_файла st;
    int дескриптор_файла;
    int root;

    дескриптор_файла = открыть("/USER2", O_RDONLY);
    report("open-readonly", дескриптор_файла >= 3);
    if (дескриптор_файла >= 0) {
        report("read-bytes", читать(дескриптор_файла, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", переместить_позицию_файла(дескриптор_файла, 0, SEEK_SET) == 0);
        report("lseek-cur", переместить_позицию_файла(дескриптор_файла, 1, SEEK_CUR) == 1);
        report("lseek-end", переместить_позицию_файла(дескриптор_файла, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", переместить_позицию_файла(дескриптор_файла, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", переместить_позицию_файла(дескриптор_файла, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", получить_состояние_открытого_файла(дескриптор_файла, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(получить_состояние_открытого_файла(дескриптор_файла, (struct состояние_файла *)0), EFAULT));
        report("fsync-file", согласовать_данные_файла(дескриптор_файла) == 0);
        report("close-file", закрыть(дескриптор_файла) == 0);
        errno = 0;
        report("closed-fd", failed_with(закрыть(дескриптор_файла), EBADF));
    }

    root = открыть("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", получить_состояние_открытого_файла(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", читать(root, bytes, 1) == -1 && errno == EISDIR);
        (void)закрыть(root);
    }

    report("fstat-character", получить_состояние_открытого_файла(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", писать(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", читать(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", читать(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", писать(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", переместить_позицию_файла(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(согласовать_данные_файла(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(открыть("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(открыть((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(открыть("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(открыть("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(открыть("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(открыть("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(открыть("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(открыть("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(создать_файл("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(закрыть(-1), EBADF));

    согласовать_все_данные();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct состояние_файла st;
    int дескриптор_файла = открыть("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (дескриптор_файла < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = дублировать_ссылку_на_открытый_файл(дескриптор_файла);
    report("dup", copy >= 0 && copy != дескриптор_файла);
    if (copy >= 0) {
        report("dup-shared-offset", читать(дескриптор_файла, &first, 1) == 1 && читать(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", закрыть(дескриптор_файла) == 0 && получить_состояние_открытого_файла(copy, &st) == 0);
        дескриптор_файла = copy;
    }

    target = дублировать_ссылку_под_заданным_номером(дескриптор_файла, 20);
    report("dup2", target == 20 && получить_состояние_открытого_файла(20, &st) == 0);
    report("dup2-same", дублировать_ссылку_под_заданным_номером(дескриптор_файла, дескриптор_файла) == дескриптор_файла);
    if (target == 20)
        (void)закрыть(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(дублировать_ссылку_под_заданным_номером(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(дублировать_ссылку_под_заданным_номером(дескриптор_файла, 99), EBADF));

    report("fcntl-getfd", управлять_файлом(дескриптор_файла, F_GETFD) == 0);
    report("fcntl-setfd", управлять_файлом(дескриптор_файла, F_SETFD, FD_CLOEXEC) == 0 &&
           управлять_файлом(дескриптор_файла, F_GETFD) == FD_CLOEXEC);
    high = управлять_файлом(дескриптор_файла, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", управлять_файлом(high, F_GETFD) == 0);
        (void)закрыть(high);
    }
    report("fcntl-getfl", (управлять_файлом(дескриптор_файла, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", управлять_файлом(дескриптор_файла, F_SETFL, O_APPEND) == 0 &&
           (управлять_файлом(дескриптор_файла, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(управлять_файлом(дескриптор_файла, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(управлять_файлом(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(дублировать_ссылку_на_открытый_файл(-1), EBADF));
    (void)закрыть(дескриптор_файла);
}

static void test_terminal_and_uname(void)
{
    struct utsname сведения_о_системе;
    int дескриптор_файла;

    report("isatty-stdin", проверить_является_ли_терминалом(STDIN_FILENO) == 1);
    report("isatty-stdout", проверить_является_ли_терминалом(STDOUT_FILENO) == 1);
    дескриптор_файла = открыть("/USER2", O_RDONLY);
    if (дескриптор_файла >= 0) {
        errno = 0;
        report("isatty-enotty", проверить_является_ли_терминалом(дескриптор_файла) == 0 && errno == ENOTTY);
        (void)закрыть(дескриптор_файла);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", проверить_является_ли_терминалом(-1) == 0 && errno == EBADF);

    report("uname", получить_сведения_о_системе(&сведения_о_системе) == 0 && сведения_о_системе.sysname[0] != 0 &&
           сведения_о_системе.nodename[0] != 0 && text_equal(сведения_о_системе.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(получить_сведения_о_системе((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)сместить_конец_динамической_памяти(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)сместить_конец_динамической_памяти(32);
    report("sbrk-grow", old == start && сместить_конец_динамической_памяти(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", задать_конец_динамической_памяти((void *)start) == 0 && сместить_конец_динамической_памяти(0) == (void *)start);
}

void posix_test_process(void)
{
    int состояние = 0;
    int дескриптор_файла;
    char byte;
    pid_t parent = получить_номер_процесса();
    pid_t child = создать_дочерний_процесс();
    pid_t waited;

    if (child == 0) {
        if (получить_номер_процесса() == parent || получить_номер_родительского_процесса() != parent)
            немедленно_завершить(90);
        немедленно_завершить(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &состояние);
        report("waitpid", waited == child && WIFEXITED(состояние) && WEXITSTATUS(состояние) == 23);
        errno = 0;
        report("waitpid-echild", ждать_указанного_потомка(child, &состояние, WNOHANG) == -1 && errno == ECHILD);
    }

    дескриптор_файла = открыть("/USER2", O_RDONLY);
    child = создать_дочерний_процесс();
    if (child == 0) {
        (void)закрыть(дескриптор_файла);
        немедленно_завершить(0);
    }
    if (child > 0 && reap_nohang(child, &состояние) == child) {
        report("fork-fd-isolation", читать(дескриптор_файла, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (дескриптор_файла >= 0)
        (void)закрыть(дескриптор_файла);

    errno = 0;
    report("execve-enoent", failed_with(заменить_исполняемую_программу("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(заменить_исполняемую_программу((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = создать_дочерний_процесс();
    if (child == 0) {
        (void)заменить_исполняемую_программу("/PXEXEC", (char *const *)0, (char *const *)0);
        немедленно_завершить(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &состояние);
        report("execve", waited == child && WIFEXITED(состояние) && WEXITSTATUS(состояние) == 37);
    }

    child = создать_дочерний_процесс();
    if (child == 0)
        немедленно_завершить(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)получить_номер_процесса();
        waited = ждать_потомка(&состояние);
        report("wait", waited == child && WIFEXITED(состояние) && WEXITSTATUS(состояние) == 29);
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
    немедленно_завершить(failures == 0 ? 0 : 1);
}
