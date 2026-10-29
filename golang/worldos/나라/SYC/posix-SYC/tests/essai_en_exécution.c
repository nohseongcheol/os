#include <errno.h>
#include <fcntl.h>
#include <système/stat.h>
#include <système/identité_du_système.h>
#include <système/attente_des_enfants.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int longueur = 0;
    while (text[longueur] != 0)
        longueur++;
    return longueur;
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
    (void)écrire(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *identité_du_système, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(identité_du_système);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *état)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = attendre_un_enfant_désigné(child, état, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", obtenir_identifiant_du_processus() > 0);
    report("getppid", obtenir_identifiant_du_parent() >= 0);
    report("getuid", obtenir_identifiant_utilisateur() == 0);
    report("geteuid", obtenir_identifiant_utilisateur_effectif() == 0);
    report("getgid", obtenir_identifiant_du_groupe() == 0);
    report("getegid", obtenir_identifiant_du_groupe_effectif() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct état_du_fichier st;

    report("getcwd", obtenir_le_chemin_du_répertoire_courant(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", obtenir_le_chemin_du_répertoire_courant(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", obtenir_le_chemin_du_répertoire_courant((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", changer_le_répertoire_courant("/") == 0);
    report("chdir-dot", changer_le_répertoire_courant(".") == 0);
    report("chdir-root-dot", changer_le_répertoire_courant("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(changer_le_répertoire_courant("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(changer_le_répertoire_courant((const char *)0), EFAULT));

    report("access-file", vérifier_les_droits_accès("/USER2", F_OK) == 0 && vérifier_les_droits_accès("/USER2", R_OK) == 0);
    report("access-root", vérifier_les_droits_accès("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(vérifier_les_droits_accès("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(vérifier_les_droits_accès("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(vérifier_les_droits_accès("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(vérifier_les_droits_accès("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(vérifier_les_droits_accès((const char *)0, F_OK), EFAULT));

    report("stat-root", état_du_fichier("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", état_du_fichier("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", obtenir_état_du_lien_même("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(état_du_fichier("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(état_du_fichier((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(état_du_fichier("/", (struct état_du_fichier *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct état_du_fichier st;
    int descripteur_de_fichier;
    int root;

    descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    report("open-readonly", descripteur_de_fichier >= 3);
    if (descripteur_de_fichier >= 0) {
        report("read-bytes", lire(descripteur_de_fichier, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", déplacer_la_position_de_fichier(descripteur_de_fichier, 0, SEEK_SET) == 0);
        report("lseek-cur", déplacer_la_position_de_fichier(descripteur_de_fichier, 1, SEEK_CUR) == 1);
        report("lseek-end", déplacer_la_position_de_fichier(descripteur_de_fichier, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", déplacer_la_position_de_fichier(descripteur_de_fichier, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", déplacer_la_position_de_fichier(descripteur_de_fichier, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", obtenir_état_du_fichier_ouvert(descripteur_de_fichier, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(obtenir_état_du_fichier_ouvert(descripteur_de_fichier, (struct état_du_fichier *)0), EFAULT));
        report("fsync-file", synchroniser_les_données_du_fichier(descripteur_de_fichier) == 0);
        report("close-file", fermer(descripteur_de_fichier) == 0);
        errno = 0;
        report("closed-fd", failed_with(fermer(descripteur_de_fichier), EBADF));
    }

    root = ouvrir("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", obtenir_état_du_fichier_ouvert(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", lire(root, bytes, 1) == -1 && errno == EISDIR);
        (void)fermer(root);
    }

    report("fstat-character", obtenir_état_du_fichier_ouvert(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", écrire(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", lire(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", lire(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", écrire(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", déplacer_la_position_de_fichier(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(synchroniser_les_données_du_fichier(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(ouvrir("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(ouvrir((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(ouvrir("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(ouvrir("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(ouvrir("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(ouvrir("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(ouvrir("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(ouvrir("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(créer_un_fichier("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(fermer(-1), EBADF));

    synchroniser_toutes_les_données();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct état_du_fichier st;
    int descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (descripteur_de_fichier < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = dupliquer_la_référence_de_fichier_ouvert(descripteur_de_fichier);
    report("dup", copy >= 0 && copy != descripteur_de_fichier);
    if (copy >= 0) {
        report("dup-shared-offset", lire(descripteur_de_fichier, &first, 1) == 1 && lire(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", fermer(descripteur_de_fichier) == 0 && obtenir_état_du_fichier_ouvert(copy, &st) == 0);
        descripteur_de_fichier = copy;
    }

    target = dupliquer_la_référence_vers_un_numéro(descripteur_de_fichier, 20);
    report("dup2", target == 20 && obtenir_état_du_fichier_ouvert(20, &st) == 0);
    report("dup2-same", dupliquer_la_référence_vers_un_numéro(descripteur_de_fichier, descripteur_de_fichier) == descripteur_de_fichier);
    if (target == 20)
        (void)fermer(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(dupliquer_la_référence_vers_un_numéro(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(dupliquer_la_référence_vers_un_numéro(descripteur_de_fichier, 99), EBADF));

    report("fcntl-getfd", contrôler_le_fichier(descripteur_de_fichier, F_GETFD) == 0);
    report("fcntl-setfd", contrôler_le_fichier(descripteur_de_fichier, F_SETFD, FD_CLOEXEC) == 0 &&
           contrôler_le_fichier(descripteur_de_fichier, F_GETFD) == FD_CLOEXEC);
    high = contrôler_le_fichier(descripteur_de_fichier, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", contrôler_le_fichier(high, F_GETFD) == 0);
        (void)fermer(high);
    }
    report("fcntl-getfl", (contrôler_le_fichier(descripteur_de_fichier, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", contrôler_le_fichier(descripteur_de_fichier, F_SETFL, O_APPEND) == 0 &&
           (contrôler_le_fichier(descripteur_de_fichier, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(contrôler_le_fichier(descripteur_de_fichier, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(contrôler_le_fichier(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(dupliquer_la_référence_de_fichier_ouvert(-1), EBADF));
    (void)fermer(descripteur_de_fichier);
}

static void test_terminal_and_uname(void)
{
    struct utsname identité_du_système;
    int descripteur_de_fichier;

    report("isatty-stdin", vérifier_si_terminal(STDIN_FILENO) == 1);
    report("isatty-stdout", vérifier_si_terminal(STDOUT_FILENO) == 1);
    descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    if (descripteur_de_fichier >= 0) {
        errno = 0;
        report("isatty-enotty", vérifier_si_terminal(descripteur_de_fichier) == 0 && errno == ENOTTY);
        (void)fermer(descripteur_de_fichier);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", vérifier_si_terminal(-1) == 0 && errno == EBADF);

    report("uname", obtenir_informations_du_système(&identité_du_système) == 0 && identité_du_système.sysname[0] != 0 &&
           identité_du_système.nodename[0] != 0 && text_equal(identité_du_système.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(obtenir_informations_du_système((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)déplacer_la_fin_de_mémoire_dynamique(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)déplacer_la_fin_de_mémoire_dynamique(32);
    report("sbrk-grow", old == start && déplacer_la_fin_de_mémoire_dynamique(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", fixer_la_fin_de_mémoire_dynamique((void *)start) == 0 && déplacer_la_fin_de_mémoire_dynamique(0) == (void *)start);
}

void posix_test_process(void)
{
    int état = 0;
    int descripteur_de_fichier;
    char byte;
    pid_t parent = obtenir_identifiant_du_processus();
    pid_t child = dédoubler_le_processus();
    pid_t waited;

    if (child == 0) {
        if (obtenir_identifiant_du_processus() == parent || obtenir_identifiant_du_parent() != parent)
            terminer_immédiatement(90);
        terminer_immédiatement(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &état);
        report("waitpid", waited == child && WIFEXITED(état) && WEXITSTATUS(état) == 23);
        errno = 0;
        report("waitpid-echild", attendre_un_enfant_désigné(child, &état, WNOHANG) == -1 && errno == ECHILD);
    }

    descripteur_de_fichier = ouvrir("/USER2", O_RDONLY);
    child = dédoubler_le_processus();
    if (child == 0) {
        (void)fermer(descripteur_de_fichier);
        terminer_immédiatement(0);
    }
    if (child > 0 && reap_nohang(child, &état) == child) {
        report("fork-fd-isolation", lire(descripteur_de_fichier, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (descripteur_de_fichier >= 0)
        (void)fermer(descripteur_de_fichier);

    errno = 0;
    report("execve-enoent", failed_with(remplacer_le_programme_exécuté("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(remplacer_le_programme_exécuté((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = dédoubler_le_processus();
    if (child == 0) {
        (void)remplacer_le_programme_exécuté("/PXEXEC", (char *const *)0, (char *const *)0);
        terminer_immédiatement(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &état);
        report("execve", waited == child && WIFEXITED(état) && WEXITSTATUS(état) == 37);
    }

    child = dédoubler_le_processus();
    if (child == 0)
        terminer_immédiatement(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)obtenir_identifiant_du_processus();
        waited = attendre_un_enfant(&état);
        report("wait", waited == child && WIFEXITED(état) && WEXITSTATUS(état) == 29);
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
    terminer_immédiatement(failures == 0 ? 0 : 1);
}
