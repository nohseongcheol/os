/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sistema/stat.h>
#include <sistema/identidad_del_sistema.h>
#include <sistema/espera_de_hijos.h>
#include <unistd.h>

static int checks;
static int failures;

static unsigned int text_length(const char *text)
{
    unsigned int longitud = 0;
    while (text[longitud] != 0)
        longitud++;
    return longitud;
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
    (void)escribir(STDOUT_FILENO, text, text_length(text));
}

static void report(const char *identidad_del_sistema, int passed)
{
    checks++;
    if (passed) {
        say("PTEST:PASS:");
    } else {
        failures++;
        say("PTEST:FAIL:");
    }
    say(identidad_del_sistema);
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
        result = esperar_hijo_indicado(child, estado, WNOHANG);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_identity(void)
{
    report("getpid", obtener_identificador_de_proceso() > 0);
    report("getppid", obtener_identificador_del_padre() >= 0);
    report("getuid", obtener_identificador_de_usuario() == 0);
    report("geteuid", obtener_identificador_efectivo_de_usuario() == 0);
    report("getgid", obtener_identificador_de_grupo() == 0);
    report("getegid", obtener_identificador_efectivo_de_grupo() == 0);
}

static void test_paths(void)
{
    char cwd[4] = {'x', 'x', 'x', 'x'};
    struct estado_del_archivo st;

    report("getcwd", obtener_ruta_del_directorio_de_trabajo(cwd, sizeof(cwd)) == cwd && cwd[0] == '/' && cwd[1] == 0);
    errno = 0;
    report("getcwd-erange", obtener_ruta_del_directorio_de_trabajo(cwd, 1) == 0 && errno == ERANGE);
    errno = 0;
    report("getcwd-efault", obtener_ruta_del_directorio_de_trabajo((char *)0, 4) == 0 && errno == EFAULT);

    report("chdir-root", cambiar_directorio_de_trabajo("/") == 0);
    report("chdir-dot", cambiar_directorio_de_trabajo(".") == 0);
    report("chdir-root-dot", cambiar_directorio_de_trabajo("/.") == 0);
    errno = 0;
    report("chdir-enotdir", failed_with(cambiar_directorio_de_trabajo("/USER2"), ENOTDIR));
    errno = 0;
    report("chdir-efault", failed_with(cambiar_directorio_de_trabajo((const char *)0), EFAULT));

    report("access-file", comprobar_permisos_de_acceso("/USER2", F_OK) == 0 && comprobar_permisos_de_acceso("/USER2", R_OK) == 0);
    report("access-root", comprobar_permisos_de_acceso("/", F_OK | R_OK | X_OK) == 0);
    errno = 0;
    report("access-write-denied", failed_with(comprobar_permisos_de_acceso("/USER2", W_OK), EACCES));
    errno = 0;
    report("access-execute-denied", failed_with(comprobar_permisos_de_acceso("/USER2", X_OK), EACCES));
    errno = 0;
    report("access-enoent", failed_with(comprobar_permisos_de_acceso("/NOFILE", F_OK), ENOENT));
    errno = 0;
    report("access-einval", failed_with(comprobar_permisos_de_acceso("/USER2", 8), EINVAL));
    errno = 0;
    report("access-efault", failed_with(comprobar_permisos_de_acceso((const char *)0, F_OK), EFAULT));

    report("stat-root", estado_del_archivo("/", &st) == 0 && S_ISDIR(st.st_mode) && st.st_nlink == 1);
    report("stat-file", estado_del_archivo("/USER2", &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
    report("lstat-file", obtener_estado_del_enlace_mismo("/USER2", &st) == 0 && S_ISREG(st.st_mode));
    errno = 0;
    report("stat-enoent", failed_with(estado_del_archivo("/NOFILE", &st), ENOENT));
    errno = 0;
    report("stat-efault-path", failed_with(estado_del_archivo((const char *)0, &st), EFAULT));
    errno = 0;
    report("stat-efault-buffer", failed_with(estado_del_archivo("/", (struct estado_del_archivo *)0), EFAULT));
}

static void test_open_and_io(void)
{
    char bytes[4];
    struct estado_del_archivo st;
    int descriptor_del_archivo;
    int root;

    descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    report("open-readonly", descriptor_del_archivo >= 3);
    if (descriptor_del_archivo >= 0) {
        report("read-bytes", leer(descriptor_del_archivo, bytes, 2) == 2 &&
               (unsigned char)bytes[0] == 0x7f && bytes[1] == 'E');
        report("lseek-set", mover_posición_del_archivo(descriptor_del_archivo, 0, SEEK_SET) == 0);
        report("lseek-cur", mover_posición_del_archivo(descriptor_del_archivo, 1, SEEK_CUR) == 1);
        report("lseek-end", mover_posición_del_archivo(descriptor_del_archivo, -1, SEEK_END) > 0);
        errno = 0;
        report("lseek-negative", mover_posición_del_archivo(descriptor_del_archivo, -1, SEEK_SET) == -1 && errno == EINVAL);
        errno = 0;
        report("lseek-whence", mover_posición_del_archivo(descriptor_del_archivo, 0, 99) == -1 && errno == EINVAL);
        report("fstat-file", obtener_estado_del_archivo_abierto(descriptor_del_archivo, &st) == 0 && S_ISREG(st.st_mode) && st.st_size > 2);
        errno = 0;
        report("fstat-efault", failed_with(obtener_estado_del_archivo_abierto(descriptor_del_archivo, (struct estado_del_archivo *)0), EFAULT));
        report("fsync-file", sincronizar_datos_del_archivo(descriptor_del_archivo) == 0);
        report("close-file", cerrar(descriptor_del_archivo) == 0);
        errno = 0;
        report("closed-fd", failed_with(cerrar(descriptor_del_archivo), EBADF));
    }

    root = abrir("/", O_RDONLY | O_DIRECTORY);
    report("open-directory", root >= 3);
    if (root >= 0) {
        report("fstat-directory", obtener_estado_del_archivo_abierto(root, &st) == 0 && S_ISDIR(st.st_mode));
        errno = 0;
        report("read-directory", leer(root, bytes, 1) == -1 && errno == EISDIR);
        (void)cerrar(root);
    }

    report("fstat-character", obtener_estado_del_archivo_abierto(STDOUT_FILENO, &st) == 0 && S_ISCHR(st.st_mode));
    report("write", escribir(STDOUT_FILENO, "", 0) == 0);
    report("read-zero", leer(STDIN_FILENO, bytes, 0) == 0);
    errno = 0;
    report("read-ebadf", leer(STDOUT_FILENO, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("write-ebadf", escribir(-1, bytes, 1) == -1 && errno == EBADF);
    errno = 0;
    report("lseek-espipe", mover_posición_del_archivo(STDOUT_FILENO, 0, SEEK_SET) == -1 && errno == ESPIPE);
    errno = 0;
    report("fsync-ebadf", failed_with(sincronizar_datos_del_archivo(-1), EBADF));

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
    report("creat-erofs", failed_with(crear_archivo("/NEWFILE", 0600), EROFS));
    errno = 0;
    report("close-ebadf", failed_with(cerrar(-1), EBADF));

    sincronizar_todos_los_datos();
    report("sync", 1);
}

static void test_dup_and_fcntl(void)
{
    char first;
    char second;
    struct estado_del_archivo st;
    int descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    int copy;
    int high;
    int target;

    if (descriptor_del_archivo < 0) {
        report("dup-setup", 0);
        return;
    }
    copy = duplicar_referencia_de_archivo_abierto(descriptor_del_archivo);
    report("dup", copy >= 0 && copy != descriptor_del_archivo);
    if (copy >= 0) {
        report("dup-shared-offset", leer(descriptor_del_archivo, &first, 1) == 1 && leer(copy, &second, 1) == 1 &&
               (unsigned char)first == 0x7f && second == 'E');
        report("dup-close-original", cerrar(descriptor_del_archivo) == 0 && obtener_estado_del_archivo_abierto(copy, &st) == 0);
        descriptor_del_archivo = copy;
    }

    target = duplicar_referencia_al_número_indicado(descriptor_del_archivo, 20);
    report("dup2", target == 20 && obtener_estado_del_archivo_abierto(20, &st) == 0);
    report("dup2-same", duplicar_referencia_al_número_indicado(descriptor_del_archivo, descriptor_del_archivo) == descriptor_del_archivo);
    if (target == 20)
        (void)cerrar(20);
    errno = 0;
    report("dup2-old-ebadf", failed_with(duplicar_referencia_al_número_indicado(-1, 10), EBADF));
    errno = 0;
    report("dup2-new-ebadf", failed_with(duplicar_referencia_al_número_indicado(descriptor_del_archivo, 99), EBADF));

    report("fcntl-getfd", controlar_archivo(descriptor_del_archivo, F_GETFD) == 0);
    report("fcntl-setfd", controlar_archivo(descriptor_del_archivo, F_SETFD, FD_CLOEXEC) == 0 &&
           controlar_archivo(descriptor_del_archivo, F_GETFD) == FD_CLOEXEC);
    high = controlar_archivo(descriptor_del_archivo, F_DUPFD, 10);
    report("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report("fcntl-fd-flags-independent", controlar_archivo(high, F_GETFD) == 0);
        (void)cerrar(high);
    }
    report("fcntl-getfl", (controlar_archivo(descriptor_del_archivo, F_GETFL) & O_ACCMODE) == O_RDONLY);
    report("fcntl-setfl", controlar_archivo(descriptor_del_archivo, F_SETFL, O_APPEND) == 0 &&
           (controlar_archivo(descriptor_del_archivo, F_GETFL) & O_APPEND) != 0);
    errno = 0;
    report("fcntl-command-einval", failed_with(controlar_archivo(descriptor_del_archivo, 999), EINVAL));
    errno = 0;
    report("fcntl-fd-ebadf", failed_with(controlar_archivo(-1, F_GETFD), EBADF));
    errno = 0;
    report("dup-ebadf", failed_with(duplicar_referencia_de_archivo_abierto(-1), EBADF));
    (void)cerrar(descriptor_del_archivo);
}

static void test_terminal_and_uname(void)
{
    struct utsname identidad_del_sistema;
    int descriptor_del_archivo;

    report("isatty-stdin", comprobar_si_es_terminal(STDIN_FILENO) == 1);
    report("isatty-stdout", comprobar_si_es_terminal(STDOUT_FILENO) == 1);
    descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    if (descriptor_del_archivo >= 0) {
        errno = 0;
        report("isatty-enotty", comprobar_si_es_terminal(descriptor_del_archivo) == 0 && errno == ENOTTY);
        (void)cerrar(descriptor_del_archivo);
    } else {
        report("isatty-enotty", 0);
    }
    errno = 0;
    report("isatty-ebadf", comprobar_si_es_terminal(-1) == 0 && errno == EBADF);

    report("uname", obtener_información_del_sistema(&identidad_del_sistema) == 0 && identidad_del_sistema.sysname[0] != 0 &&
           identidad_del_sistema.nodename[0] != 0 && text_equal(identidad_del_sistema.machine, "i386"));
    errno = 0;
    report("uname-efault", failed_with(obtener_información_del_sistema((struct utsname *)0), EFAULT));
}

void posix_test_heap(void)
{
    volatile unsigned char *start = (volatile unsigned char *)mover_fin_de_memoria_dinámica(0);
    volatile unsigned char *old;

    report("sbrk-query", start != (void *)-1 && start != (void *)0);
    old = (volatile unsigned char *)mover_fin_de_memoria_dinámica(32);
    report("sbrk-grow", old == start && mover_fin_de_memoria_dinámica(0) == (void *)(start + 32));
    if (old != (void *)-1) {
        old[0] = 0x5a;
        old[31] = 0xa5;
        report("sbrk-memory", old[0] == 0x5a && old[31] == 0xa5);
    }
    report("brk-restore", fijar_fin_de_memoria_dinámica((void *)start) == 0 && mover_fin_de_memoria_dinámica(0) == (void *)start);
}

void posix_test_process(void)
{
    int estado = 0;
    int descriptor_del_archivo;
    char byte;
    pid_t parent = obtener_identificador_de_proceso();
    pid_t child = bifurcar_proceso();
    pid_t waited;

    if (child == 0) {
        if (obtener_identificador_de_proceso() == parent || obtener_identificador_del_padre() != parent)
            terminar_inmediatamente(90);
        terminar_inmediatamente(23);
    }
    report("fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &estado);
        report("waitpid", waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 23);
        errno = 0;
        report("waitpid-echild", esperar_hijo_indicado(child, &estado, WNOHANG) == -1 && errno == ECHILD);
    }

    descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    child = bifurcar_proceso();
    if (child == 0) {
        (void)cerrar(descriptor_del_archivo);
        terminar_inmediatamente(0);
    }
    if (child > 0 && reap_nohang(child, &estado) == child) {
        report("fork-fd-isolation", leer(descriptor_del_archivo, &byte, 1) == 1 && (unsigned char)byte == 0x7f);
    } else {
        report("fork-fd-isolation", 0);
    }
    if (descriptor_del_archivo >= 0)
        (void)cerrar(descriptor_del_archivo);

    errno = 0;
    report("execve-enoent", failed_with(sustituir_programa_en_ejecución("/NOFILE", (char *const *)0,
                                                (char *const *)0), ENOENT));
    errno = 0;
    report("execve-efault", failed_with(sustituir_programa_en_ejecución((const char *)0, (char *const *)0,
                                                (char *const *)0), EFAULT));

    child = bifurcar_proceso();
    if (child == 0) {
        (void)sustituir_programa_en_ejecución("/PXEXEC", (char *const *)0, (char *const *)0);
        terminar_inmediatamente(91);
    }
    report("execve-fork", child > 0);
    if (child > 0) {
        waited = reap_nohang(child, &estado);
        report("execve", waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 37);
    }

    child = bifurcar_proceso();
    if (child == 0)
        terminar_inmediatamente(29);
    report("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin;
        for (spin = 0; spin < 2000000U; spin++)
            (void)obtener_identificador_de_proceso();
        waited = esperar_hijo(&estado);
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
    terminar_inmediatamente(failures == 0 ? 0 : 1);
}
