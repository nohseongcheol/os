#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int lunghezza = 0;
    while (text[lunghezza] != 0)
        lunghezza++;
    return lunghezza;
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
    (void)Scrittura(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *identità_del_sistema, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(identità_del_sistema);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *stato)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = waitpid(child, stato, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", getpid() > 0);
    report("getppid", getppid() >= 0);
    report("getuid", getuid() == 0);
    report("geteuid", geteuid() == 0);
    report("getgid", getgid() == 0);
    report("getegid", getegid() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct stat st;

    report("getcwd", getcwd(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", getcwd(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", getcwd((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", chdir("/") == 0);
    report("chdir-dot", chdir(".") == 0);
    report("chdir-root-dot", chdir("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(chdir("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(chdir((const char *)0), EFAULT));

    report("access-file", access("/USER2", F_OK) == 0 && access("/USER2", R_OK) == 0);
    report("access-root", access("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(access("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(access("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(access("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(access("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(access((const char *)0, F_OK), EFAULT));

    report("stat-root", stat("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", stat("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", lstat("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(stat("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(stat((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(stat("/", (struct stat *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct stat st;
    int descrittore_del_file;
    int root;

    descrittore_del_file = Apri("/USER2", O_RDONLY);
    report("open-readonly", descrittore_del_file >= 3);
    if (descrittore_del_file >= 0) {
        report("read-bytes", Lettura(descrittore_del_file, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", lseek(descrittore_del_file, 0, SEEK_SET) == 0);
        report("lseek-cur", lseek(descrittore_del_file, 1, SEEK_CUR) == 1);
        report("lseek-end", lseek(descrittore_del_file, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", lseek(descrittore_del_file, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", lseek(descrittore_del_file, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", fstat(descrittore_del_file, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(fstat(descrittore_del_file, (struct stat *)0), EFAULT));
        report("fsync-file", fsync(descrittore_del_file) == 0);
        report("close-file", Chiudi(descrittore_del_file) == 0);
        errno = 0;
        report("closed-fd", failed_with(Chiudi(descrittore_del_file), EBADF));
    }

    root = Apri("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", fstat(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", Lettura(root, bytes, 1) == -1 && errno == EISDIR);
        (void)Chiudi(root);
    }

    report("fstat-character", fstat(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", Scrittura(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", Lettura(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", Lettura(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", Scrittura(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", lseek(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(fsync(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(Apri("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(Apri((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(Apri("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(Apri("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(Apri("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(Apri("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(Apri("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(Apri("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(creat("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(Chiudi(-1), EBADF));

    sync();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct stat st;
    int descrittore_del_file = Apri("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (descrittore_del_file < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = dup(descrittore_del_file);
    report("dup", copy >= 0 && copy != descrittore_del_file);
    if (copy >= 0) {
        report("dup-shared-offset", Lettura(descrittore_del_file, &first, 1) == 1 && Lettura(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", Chiudi(descrittore_del_file) == 0 && fstat(copy, &st) == 0);
        descrittore_del_file = copy;
    }

    target = dup2(descrittore_del_file, 20);
    report("dup2", target == 20 && fstat(20, &st) == 0);
    report("dup2-same", dup2(descrittore_del_file, descrittore_del_file) == descrittore_del_file);
    if (target == 20)
        (void)Chiudi(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(dup2(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(dup2(descrittore_del_file, 99), EBADF));

    report("fcntl-getfd", fcntl(descrittore_del_file, F_GETFD) == 0);
    report("fcntl-setfd", fcntl(descrittore_del_file, F_SETFD, FD_CLOEXEC) == 0 &&
           fcntl(descrittore_del_file, F_GETFD) == FD_CLOEXEC);
    high = fcntl(descrittore_del_file, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", fcntl(high, F_GETFD) == 0);
        (void)Chiudi(high);
    }
    report("fcntl-getfl", (fcntl(descrittore_del_file, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", fcntl(descrittore_del_file, F_SETFL, O_APPEND) == 0 &&
           (fcntl(descrittore_del_file, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(fcntl(descrittore_del_file, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(fcntl(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(dup(-1), EBADF));
    (void)Chiudi(descrittore_del_file);
}

static void test_terminal_and_uname(void)
{
    struct utsname identità_del_sistema;
    int descrittore_del_file;

    report("isatty-stdin", isatty(STDIN_FILENO) == 1);
    report("isatty-stdout", isatty(STDOUT_FILENO) == 1);
    descrittore_del_file = Apri("/USER2", O_RDONLY);
    if (descrittore_del_file >= 0) {
        errno = 0;
        report("isatty-enotty", isatty(descrittore_del_file) == 0 && errno == ENOTTY);
        (void)Chiudi(descrittore_del_file);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", isatty(-1) == 0 && errno == EBADF);

    report("uname", uname(&identità_del_sistema) == 0 && identità_del_sistema.sysname[0] != 0 &&
           identità_del_sistema.nodename[0] != 0 && text_equal(identità_del_sistema.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(uname((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)sbrk(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)sbrk(32);
    report("sbrk-grow", old == start && sbrk(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", brk((void *)start) == 0 && sbrk(0) == (void *)start);
}

void posix_test_process(void)
{
    int stato = 0;
    int descrittore_del_file;
    char byte;
    pid_t parent = getpid();
    pid_t child = fork();
    pid_t waited;

    if (child == 0) {
        if (getpid() == parent || getppid() != parent)
            _exit(90);
        _exit(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &stato);
        report("waitpid", waited == child && WIFEXITED(stato) && WEXITSTATUS(stato) == 23);
        errno = 0;
        report("waitpid-echild", waitpid(child, &stato, WNOHANG) == -1 && errno == ECHILD);
    }

    descrittore_del_file = Apri("/USER2", O_RDONLY);
    child = fork();
    if (child == 0) {
        (void)Chiudi(descrittore_del_file);
        _exit(0);
    }
    if (child > 0 && reap_nohang(child, &stato) == child) {
        report("fork-fd-isolation", Lettura(descrittore_del_file, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (descrittore_del_file >= 0)
        (void)Chiudi(descrittore_del_file);

    errno = 0;
    report("execve-enoent", failed_with(execve("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(execve((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = fork();
    if (child == 0) {
        (void)execve("/PXEXEC", (char *const *)0, (char *const *)0);
        _exit(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &stato);
        report("execve", waited == child && WIFEXITED(stato) && WEXITSTATUS(stato) == 37);
    }

    child = fork();
    if (child == 0)
        _exit(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)getpid();
        waited = wait(&stato);
        report("wait", waited == child && WIFEXITED(stato) && WEXITSTATUS(stato) == 29);
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
    _exit(failures == 0 ? 0 : 1);
}
