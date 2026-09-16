#include <errno.h>
#include <fcntl.h>
#include <sistema/stat.h>
#include <sistema/identidade_do_sistema.h>
#include <sistema/espera_de_filhos.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int comprimento = 0;
    while (text[comprimento] != 0)
        comprimento++;
    return comprimento;
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
    (void)escrever(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *identidade_do_sistema, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(identidade_do_sistema);
    say("\n");
}

static int failed_with(int result, int expected_errno)
{
    return result == -1 && errno == expected_errno;
}

static pid_t reap_nohang(pid_t child, int *estado)
{
    unsigned int spins;
    pid_t result;

    for (spins = 0; spins < 2000000U; spins++) {
        result = aguardar_filho_indicado(child, estado, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", obter_identificador_do_processo() > 0);
    report("getppid", obter_identificador_do_processo_pai() >= 0);
    report("getuid", obter_identificador_do_utilizador() == 0);
    report("geteuid", obter_identificador_efetivo_do_utilizador() == 0);
    report("getgid", obter_identificador_do_grupo() == 0);
    report("getegid", obter_identificador_efetivo_do_grupo() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct estado_do_ficheiro st;

    report("getcwd", obter_caminho_do_diretório_de_trabalho(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", obter_caminho_do_diretório_de_trabalho(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", obter_caminho_do_diretório_de_trabalho((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", mudar_diretório_de_trabalho("/") == 0);
    report("chdir-dot", mudar_diretório_de_trabalho(".") == 0);
    report("chdir-root-dot", mudar_diretório_de_trabalho("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(mudar_diretório_de_trabalho("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(mudar_diretório_de_trabalho((const char *)0), EFAULT));

    report("access-file", verificar_permissões_de_acesso("/USER2", F_OK) == 0 && verificar_permissões_de_acesso("/USER2", R_OK) == 0);
    report("access-root", verificar_permissões_de_acesso("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(verificar_permissões_de_acesso("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(verificar_permissões_de_acesso("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(verificar_permissões_de_acesso("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(verificar_permissões_de_acesso("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(verificar_permissões_de_acesso((const char *)0, F_OK), EFAULT));

    report("stat-root", estado_do_ficheiro("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", estado_do_ficheiro("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", obter_estado_da_ligação_em_si("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(estado_do_ficheiro("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(estado_do_ficheiro((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(estado_do_ficheiro("/", (struct estado_do_ficheiro *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct estado_do_ficheiro st;
    int descritor_do_ficheiro;
    int root;

    descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    report("open-readonly", descritor_do_ficheiro >= 3);
    if (descritor_do_ficheiro >= 0) {
        report("read-bytes", ler(descritor_do_ficheiro, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", mover_posição_do_ficheiro(descritor_do_ficheiro, 0, SEEK_SET) == 0);
        report("lseek-cur", mover_posição_do_ficheiro(descritor_do_ficheiro, 1, SEEK_CUR) == 1);
        report("lseek-end", mover_posição_do_ficheiro(descritor_do_ficheiro, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", mover_posição_do_ficheiro(descritor_do_ficheiro, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", mover_posição_do_ficheiro(descritor_do_ficheiro, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", obter_estado_do_ficheiro_aberto(descritor_do_ficheiro, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(obter_estado_do_ficheiro_aberto(descritor_do_ficheiro, (struct estado_do_ficheiro *)0), EFAULT));
        report("fsync-file", sincronizar_dados_do_ficheiro(descritor_do_ficheiro) == 0);
        report("close-file", fechar(descritor_do_ficheiro) == 0);
        errno = 0;
        report("closed-fd", failed_with(fechar(descritor_do_ficheiro), EBADF));
    }

    root = abrir("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", obter_estado_do_ficheiro_aberto(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", ler(root, bytes, 1) == -1 && errno == EISDIR);
        (void)fechar(root);
    }

    report("fstat-character", obter_estado_do_ficheiro_aberto(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", escrever(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", ler(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", ler(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", escrever(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", mover_posição_do_ficheiro(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(sincronizar_dados_do_ficheiro(-1), EBADF));

    errno = 0;
    report("open-enoent", failed_with(abrir("/NOFILE", O_RDONLY), ENOENT));
    errno = 0;
    report("open-efault", failed_with(abrir((const char *)0, O_RDONLY), EFAULT));
    errno = 0;
    report("open-write-erofs", failed_with(abrir("/USER2", O_WRONLY), EROFS));
    errno = 0;
    report("open-rdwr-erofs", failed_with(abrir("/USER2", O_RDWR), EROFS));
    errno = 0;
    report("open-create-erofs", failed_with(abrir("/NEWFILE", O_CREAT | O_WRONLY, 0600), EROFS));
    errno = 0;
    report("open-trunc-erofs", failed_with(abrir("/USER2", O_TRUNC | O_RDONLY), EROFS));
    errno = 0;
    report("open-append-erofs", failed_with(abrir("/USER2", O_APPEND | O_RDONLY), EROFS));
    errno = 0;
    report("open-enotdir", failed_with(abrir("/USER2", O_RDONLY | O_DIRECTORY), ENOTDIR));
    errno = 0;
    report("creat-erofs", failed_with(criar_ficheiro("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(fechar(-1), EBADF));

    sincronizar_todos_os_dados();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct estado_do_ficheiro st;
    int descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (descritor_do_ficheiro < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = duplicar_referência_de_ficheiro_aberto(descritor_do_ficheiro);
    report("dup", copy >= 0 && copy != descritor_do_ficheiro);
    if (copy >= 0) {
        report("dup-shared-offset", ler(descritor_do_ficheiro, &first, 1) == 1 && ler(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", fechar(descritor_do_ficheiro) == 0 && obter_estado_do_ficheiro_aberto(copy, &st) == 0);
        descritor_do_ficheiro = copy;
    }

    target = duplicar_referência_para_número_indicado(descritor_do_ficheiro, 20);
    report("dup2", target == 20 && obter_estado_do_ficheiro_aberto(20, &st) == 0);
    report("dup2-same", duplicar_referência_para_número_indicado(descritor_do_ficheiro, descritor_do_ficheiro) == descritor_do_ficheiro);
    if (target == 20)
        (void)fechar(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(duplicar_referência_para_número_indicado(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(duplicar_referência_para_número_indicado(descritor_do_ficheiro, 99), EBADF));

    report("fcntl-getfd", controlar_ficheiro(descritor_do_ficheiro, F_GETFD) == 0);
    report("fcntl-setfd", controlar_ficheiro(descritor_do_ficheiro, F_SETFD, FD_CLOEXEC) == 0 &&
           controlar_ficheiro(descritor_do_ficheiro, F_GETFD) == FD_CLOEXEC);
    high = controlar_ficheiro(descritor_do_ficheiro, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", controlar_ficheiro(high, F_GETFD) == 0);
        (void)fechar(high);
    }
    report("fcntl-getfl", (controlar_ficheiro(descritor_do_ficheiro, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", controlar_ficheiro(descritor_do_ficheiro, F_SETFL, O_APPEND) == 0 &&
           (controlar_ficheiro(descritor_do_ficheiro, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(controlar_ficheiro(descritor_do_ficheiro, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(controlar_ficheiro(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(duplicar_referência_de_ficheiro_aberto(-1), EBADF));
    (void)fechar(descritor_do_ficheiro);
}

static void test_terminal_and_uname(void)
{
    struct utsname identidade_do_sistema;
    int descritor_do_ficheiro;

    report("isatty-stdin", verificar_se_é_terminal(STDIN_FILENO) == 1);
    report("isatty-stdout", verificar_se_é_terminal(STDOUT_FILENO) == 1);
    descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    if (descritor_do_ficheiro >= 0) {
        errno = 0;
        report("isatty-enotty", verificar_se_é_terminal(descritor_do_ficheiro) == 0 && errno == ENOTTY);
        (void)fechar(descritor_do_ficheiro);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", verificar_se_é_terminal(-1) == 0 && errno == EBADF);

    report("uname", obter_informações_do_sistema(&identidade_do_sistema) == 0 && identidade_do_sistema.sysname[0] != 0 &&
           identidade_do_sistema.nodename[0] != 0 && text_equal(identidade_do_sistema.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(obter_informações_do_sistema((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)mover_fim_da_memória_dinâmica(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)mover_fim_da_memória_dinâmica(32);
    report("sbrk-grow", old == start && mover_fim_da_memória_dinâmica(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", definir_fim_da_memória_dinâmica((void *)start) == 0 && mover_fim_da_memória_dinâmica(0) == (void *)start);
}

void posix_test_process(void)
{
    int estado = 0;
    int descritor_do_ficheiro;
    char byte;
    pid_t parent = obter_identificador_do_processo();
    pid_t child = bifurcar_processo();
    pid_t waited;

    if (child == 0) {
        if (obter_identificador_do_processo() == parent || obter_identificador_do_processo_pai() != parent)
            terminar_imediatamente(90);
        terminar_imediatamente(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &estado);
        report("waitpid", waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 23);
        errno = 0;
        report("waitpid-echild", aguardar_filho_indicado(child, &estado, WNOHANG) == -1 && errno == ECHILD);
    }

    descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    child = bifurcar_processo();
    if (child == 0) {
        (void)fechar(descritor_do_ficheiro);
        terminar_imediatamente(0);
    }
    if (child > 0 && reap_nohang(child, &estado) == child) {
        report("fork-fd-isolation", ler(descritor_do_ficheiro, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (descritor_do_ficheiro >= 0)
        (void)fechar(descritor_do_ficheiro);

    errno = 0;
    report("execve-enoent", failed_with(substituir_programa_em_execução("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(substituir_programa_em_execução((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = bifurcar_processo();
    if (child == 0) {
        (void)substituir_programa_em_execução("/PXEXEC", (char *const *)0, (char *const *)0);
        terminar_imediatamente(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &estado);
        report("execve", waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 37);
    }

    child = bifurcar_processo();
    if (child == 0)
        terminar_imediatamente(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)obter_identificador_do_processo();
        waited = aguardar_filho(&estado);
        report("wait", waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 29);
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
    terminar_imediatamente(failures == 0 ? 0 : 1);
}
