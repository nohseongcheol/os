/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <System/stat.h>
#include <System/Systemkennung.h>
#include <System/Kindwartung.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int Länge = 0;
    while (text[Länge] != 0)
        Länge++;
    return Länge;
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
    (void)schreiben(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *Systemidentität, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(Systemidentität);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *Status)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = bestimmtes_Kind_abwarten(child, Status, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", Prozesskennung_ermitteln() > 0);
    report("getppid", Elternprozesskennung_ermitteln() >= 0);
    report("getuid", Benutzerkennung_ermitteln() == 0);
    report("geteuid", wirksame_Benutzerkennung_ermitteln() == 0);
    report("getgid", Gruppenkennung_ermitteln() == 0);
    report("getegid", wirksame_Gruppenkennung_ermitteln() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct Dateizustand st;

    report("getcwd", Arbeitsverzeichnispfad_ermitteln(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", Arbeitsverzeichnispfad_ermitteln(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", Arbeitsverzeichnispfad_ermitteln((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", Arbeitsverzeichnis_wechseln("/") == 0);
    report("chdir-dot", Arbeitsverzeichnis_wechseln(".") == 0);
    report("chdir-root-dot", Arbeitsverzeichnis_wechseln("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(Arbeitsverzeichnis_wechseln("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(Arbeitsverzeichnis_wechseln((const char *)0), EFAULT));

    report("access-file", Zugriffsrechte_prüfen("/USER2", F_OK) == 0 && Zugriffsrechte_prüfen("/USER2", R_OK) == 0);
    report("access-root", Zugriffsrechte_prüfen("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(Zugriffsrechte_prüfen("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(Zugriffsrechte_prüfen("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(Zugriffsrechte_prüfen("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(Zugriffsrechte_prüfen("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(Zugriffsrechte_prüfen((const char *)0, F_OK), EFAULT));

    report("stat-root", Dateizustand("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", Dateizustand("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", Verknüpfungszustand_ermitteln("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(Dateizustand("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(Dateizustand((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(Dateizustand("/", (struct Dateizustand *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct Dateizustand st;
    int Dateideskriptor;
    int root;

    Dateideskriptor = öffnen("/USER2", O_RDONLY);
    report("open-readonly", Dateideskriptor >= 3);
    if (Dateideskriptor >= 0) {
        report("read-bytes", lesen(Dateideskriptor, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", Dateiposition_verschieben(Dateideskriptor, 0, SEEK_SET) == 0);
        report("lseek-cur", Dateiposition_verschieben(Dateideskriptor, 1, SEEK_CUR) == 1);
        report("lseek-end", Dateiposition_verschieben(Dateideskriptor, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", Dateiposition_verschieben(Dateideskriptor, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", Dateiposition_verschieben(Dateideskriptor, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", Zustand_offener_Datei_ermitteln(Dateideskriptor, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(Zustand_offener_Datei_ermitteln(Dateideskriptor, (struct Dateizustand *)0), EFAULT));
        report("fsync-file", Dateidaten_synchronisieren(Dateideskriptor) == 0);
        report("close-file", schließen(Dateideskriptor) == 0);
        errno = 0;
        report("closed-fd", failed_with(schließen(Dateideskriptor), EBADF));
    }

    root = öffnen("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", Zustand_offener_Datei_ermitteln(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", lesen(root, bytes, 1) == -1 && errno == EISDIR);
        (void)schließen(root);
    }

    report("fstat-character", Zustand_offener_Datei_ermitteln(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", schreiben(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", lesen(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", lesen(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", schreiben(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", Dateiposition_verschieben(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(Dateidaten_synchronisieren(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(öffnen("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(öffnen((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(öffnen("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(öffnen("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(öffnen("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(öffnen("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(öffnen("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(öffnen("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(Datei_anlegen("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(schließen(-1), EBADF));

    alle_Dateidaten_synchronisieren();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct Dateizustand st;
    int Dateideskriptor = öffnen("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (Dateideskriptor < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = offenen_Dateiverweis_duplizieren(Dateideskriptor);
    report("dup", copy >= 0 && copy != Dateideskriptor);
    if (copy >= 0) {
        report("dup-shared-offset", lesen(Dateideskriptor, &first, 1) == 1 && lesen(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", schließen(Dateideskriptor) == 0 && Zustand_offener_Datei_ermitteln(copy, &st) == 0);
        Dateideskriptor = copy;
    }

    target = Dateiverweis_auf_Kennung_duplizieren(Dateideskriptor, 20);
    report("dup2", target == 20 && Zustand_offener_Datei_ermitteln(20, &st) == 0);
    report("dup2-same", Dateiverweis_auf_Kennung_duplizieren(Dateideskriptor, Dateideskriptor) == Dateideskriptor);
    if (target == 20)
        (void)schließen(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(Dateiverweis_auf_Kennung_duplizieren(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(Dateiverweis_auf_Kennung_duplizieren(Dateideskriptor, 99), EBADF));

    report("fcntl-getfd", Dateizugriff_steuern(Dateideskriptor, F_GETFD) == 0);
    report("fcntl-setfd", Dateizugriff_steuern(Dateideskriptor, F_SETFD, FD_CLOEXEC) == 0 &&
           Dateizugriff_steuern(Dateideskriptor, F_GETFD) == FD_CLOEXEC);
    high = Dateizugriff_steuern(Dateideskriptor, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", Dateizugriff_steuern(high, F_GETFD) == 0);
        (void)schließen(high);
    }
    report("fcntl-getfl", (Dateizugriff_steuern(Dateideskriptor, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", Dateizugriff_steuern(Dateideskriptor, F_SETFL, O_APPEND) == 0 &&
           (Dateizugriff_steuern(Dateideskriptor, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(Dateizugriff_steuern(Dateideskriptor, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(Dateizugriff_steuern(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(offenen_Dateiverweis_duplizieren(-1), EBADF));
    (void)schließen(Dateideskriptor);
}

static void test_terminal_and_uname(void)
{
    struct utsname Systemidentität;
    int Dateideskriptor;

    report("isatty-stdin", Terminal_prüfen(STDIN_FILENO) == 1);
    report("isatty-stdout", Terminal_prüfen(STDOUT_FILENO) == 1);
    Dateideskriptor = öffnen("/USER2", O_RDONLY);
    if (Dateideskriptor >= 0) {
        errno = 0;
        report("isatty-enotty", Terminal_prüfen(Dateideskriptor) == 0 && errno == ENOTTY);
        (void)schließen(Dateideskriptor);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", Terminal_prüfen(-1) == 0 && errno == EBADF);

    report("uname", Systeminformationen_ermitteln(&Systemidentität) == 0 && Systemidentität.sysname[0] != 0 &&
           Systemidentität.nodename[0] != 0 && text_equal(Systemidentität.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(Systeminformationen_ermitteln((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)Speicherende_verschieben(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)Speicherende_verschieben(32);
    report("sbrk-grow", old == start && Speicherende_verschieben(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", Speicherende_setzen((void *)start) == 0 && Speicherende_verschieben(0) == (void *)start);
}

void posix_test_process(void)
{
    int Status = 0;
    int Dateideskriptor;
    char byte;
    pid_t parent = Prozesskennung_ermitteln();
    pid_t child = Prozess_verzweigen();
    pid_t waited;

    if (child == 0) {
        if (Prozesskennung_ermitteln() == parent || Elternprozesskennung_ermitteln() != parent)
            sofort_beenden(90);
        sofort_beenden(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &Status);
        report("waitpid", waited == child && WIFEXITED(Status) && WEXITSTATUS(Status) == 23);
        errno = 0;
        report("waitpid-echild", bestimmtes_Kind_abwarten(child, &Status, WNOHANG) == -1 && errno == ECHILD);
    }

    Dateideskriptor = öffnen("/USER2", O_RDONLY);
    child = Prozess_verzweigen();
    if (child == 0) {
        (void)schließen(Dateideskriptor);
        sofort_beenden(0);
    }
    if (child > 0 && reap_nohang(child, &Status) == child) {
        report("fork-fd-isolation", lesen(Dateideskriptor, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (Dateideskriptor >= 0)
        (void)schließen(Dateideskriptor);

    errno = 0;
    report("execve-enoent", failed_with(Programmbild_ersetzen("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(Programmbild_ersetzen((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = Prozess_verzweigen();
    if (child == 0) {
        (void)Programmbild_ersetzen("/PXEXEC", (char *const *)0, (char *const *)0);
        sofort_beenden(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &Status);
        report("execve", waited == child && WIFEXITED(Status) && WEXITSTATUS(Status) == 37);
    }

    child = Prozess_verzweigen();
    if (child == 0)
        sofort_beenden(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)Prozesskennung_ermitteln();
        waited = Kind_abwarten(&Status);
        report("wait", waited == child && WIFEXITED(Status) && WEXITSTATUS(Status) == 29);
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
    sofort_beenden(failures == 0 ? 0 : 1);
}
