/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sistema/stat.h>
#include <sistema/espera_de_hijos.h>
#include <unistd.h>
#include <sistema/syscall.h>

enum {
    SYS_terminar_inmediatamente = 1,
    SYS_bifurcar_proceso = 2,
    SYS_leer = 3,
    SYS_escribir = 4,
    SYS_cerrar = 6,
    SYS_sustituir_programa_en_ejecución = 11,
    SYS_cambiar_directorio_de_trabajo = 12,
    SYS_mover_posición_del_archivo = 19,
    SYS_obtener_identificador_de_proceso = 20,
    SYS_obtener_identificador_de_usuario = 24,
    SYS_comprobar_permisos_de_acceso = 33,
    SYS_sincronizar_todos_los_datos = 36,
    SYS_duplicar_referencia_de_archivo_abierto = 41,
    SYS_fijar_fin_de_memoria_dinámica = 45,
    SYS_obtener_identificador_de_grupo = 47,
    SYS_obtener_identificador_efectivo_de_usuario = 49,
    SYS_obtener_identificador_efectivo_de_grupo = 50,
    SYS_duplicar_referencia_al_número_indicado = 63,
    SYS_obtener_identificador_del_padre = 64,
    SYS_sincronizar_datos_del_archivo = 118,
    SYS_obtener_ruta_del_directorio_de_trabajo = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void terminar_inmediatamente(int estado)
{
    SC1(SYS_terminar_inmediatamente, estado);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t leer(int descriptor_del_archivo, void *memoria_intermedia_de_transferencia, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_leer, descriptor_del_archivo, memoria_intermedia_de_transferencia, count));
}

ssize_t escribir(int descriptor_del_archivo, const void *memoria_intermedia_de_transferencia, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_escribir, descriptor_del_archivo, memoria_intermedia_de_transferencia, count));
}

int cerrar(int descriptor_del_archivo)
{
    return (int)__syscall_result(SC1(SYS_cerrar, descriptor_del_archivo));
}

off_t mover_posición_del_archivo(int descriptor_del_archivo, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_mover_posición_del_archivo, descriptor_del_archivo, offset, whence));
}

pid_t bifurcar_proceso(void)
{
    return (pid_t)__syscall_result(SC0(SYS_bifurcar_proceso));
}

int sustituir_programa_en_ejecución(const char *ruta, char *const argumentos_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_sustituir_programa_en_ejecución, ruta, argumentos_2, envp));
}

pid_t obtener_identificador_de_proceso(void) { return (pid_t)SC0(SYS_obtener_identificador_de_proceso); }
pid_t obtener_identificador_del_padre(void) { return (pid_t)SC0(SYS_obtener_identificador_del_padre); }
uid_t obtener_identificador_de_usuario(void) { return (uid_t)SC0(SYS_obtener_identificador_de_usuario); }
uid_t obtener_identificador_efectivo_de_usuario(void) { return (uid_t)SC0(SYS_obtener_identificador_efectivo_de_usuario); }
gid_t obtener_identificador_de_grupo(void) { return (gid_t)SC0(SYS_obtener_identificador_de_grupo); }
gid_t obtener_identificador_efectivo_de_grupo(void) { return (gid_t)SC0(SYS_obtener_identificador_efectivo_de_grupo); }

int comprobar_permisos_de_acceso(const char *ruta, int mode)
{
    return (int)__syscall_result(SC2(SYS_comprobar_permisos_de_acceso, ruta, mode));
}

int cambiar_directorio_de_trabajo(const char *ruta)
{
    return (int)__syscall_result(SC1(SYS_cambiar_directorio_de_trabajo, ruta));
}

char *obtener_ruta_del_directorio_de_trabajo(char *memoria_intermedia_de_transferencia, size_t cantidad_de_dígitos)
{
    long result = __syscall_result(SC2(SYS_obtener_ruta_del_directorio_de_trabajo, memoria_intermedia_de_transferencia, cantidad_de_dígitos));
    return result < 0 ? (char *)0 : memoria_intermedia_de_transferencia;
}

int duplicar_referencia_de_archivo_abierto(int descriptor_del_archivo)
{
    return (int)__syscall_result(SC1(SYS_duplicar_referencia_de_archivo_abierto, descriptor_del_archivo));
}

int duplicar_referencia_al_número_indicado(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_duplicar_referencia_al_número_indicado, oldfd, newfd));
}

int sincronizar_datos_del_archivo(int descriptor_del_archivo)
{
    return (int)__syscall_result(SC1(SYS_sincronizar_datos_del_archivo, descriptor_del_archivo));
}

void sincronizar_todos_los_datos(void)
{
    SC0(SYS_sincronizar_todos_los_datos);
}

int comprobar_si_es_terminal(int descriptor_del_archivo)
{
    struct estado_del_archivo st;
    if (obtener_estado_del_archivo_abierto(descriptor_del_archivo, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int fijar_fin_de_memoria_dinámica(void *address)
{
    long result = SC1(SYS_fijar_fin_de_memoria_dinámica, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *mover_fin_de_memoria_dinámica(int increment)
{
    long current = SC1(SYS_fijar_fin_de_memoria_dinámica, 0);
    long requested = current + increment;
    if (increment != 0 && fijar_fin_de_memoria_dinámica((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t esperar_hijo_indicado(pid_t pid, int *estado, int options)
{
    long result;
    do {
        result = SC3(7, pid, estado, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t esperar_hijo(int *estado)
{
    return esperar_hijo_indicado(-1, estado, 0);
}
