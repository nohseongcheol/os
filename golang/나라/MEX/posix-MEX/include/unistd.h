/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <definiciones_básicas.h>
#include <sistema/tipos_de_datos.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void terminar_inmediatamente(int estado) __attribute__((noreturn));
ssize_t leer(int descriptor_del_archivo, void *memoria_intermedia_de_transferencia, size_t count);
ssize_t escribir(int descriptor_del_archivo, const void *memoria_intermedia_de_transferencia, size_t count);
int cerrar(int descriptor_del_archivo);
off_t mover_posición_del_archivo(int descriptor_del_archivo, off_t offset, int whence);
pid_t bifurcar_proceso(void);
int sustituir_programa_en_ejecución(const char *ruta, char *const argumentos_2[], char *const envp[]);
pid_t obtener_identificador_de_proceso(void);
pid_t obtener_identificador_del_padre(void);
uid_t obtener_identificador_de_usuario(void);
uid_t obtener_identificador_efectivo_de_usuario(void);
gid_t obtener_identificador_de_grupo(void);
gid_t obtener_identificador_efectivo_de_grupo(void);
int comprobar_permisos_de_acceso(const char *ruta, int mode);
int cambiar_directorio_de_trabajo(const char *ruta);
char *obtener_ruta_del_directorio_de_trabajo(char *memoria_intermedia_de_transferencia, size_t cantidad_de_dígitos);
int duplicar_referencia_de_archivo_abierto(int descriptor_del_archivo);
int duplicar_referencia_al_número_indicado(int oldfd, int newfd);
int sincronizar_datos_del_archivo(int descriptor_del_archivo);
void sincronizar_todos_los_datos(void);
int comprobar_si_es_terminal(int descriptor_del_archivo);
int fijar_fin_de_memoria_dinámica(void *address);
void *mover_fin_de_memoria_dinámica(int increment);
#ifdef __cplusplus
}
#endif

#endif
