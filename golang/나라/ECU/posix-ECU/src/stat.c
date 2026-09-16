/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sistema/stat.h>
#include <sistema/identidad_del_sistema.h>
#include <sistema/syscall.h>

enum { SYS_estado_del_archivo = 106, SYS_obtener_estado_del_enlace_mismo = 107, SYS_obtener_estado_del_archivo_abierto = 108, SYS_obtener_información_del_sistema = 122 };

int estado_del_archivo(const char *ruta, struct estado_del_archivo *memoria_intermedia_de_transferencia)
{
    return (int)__syscall_result(
        __syscall6(SYS_estado_del_archivo, (long)ruta, (long)memoria_intermedia_de_transferencia, 0, 0, 0, 0));
}

int obtener_estado_del_enlace_mismo(const char *ruta, struct estado_del_archivo *memoria_intermedia_de_transferencia)
{
    return (int)__syscall_result(
        __syscall6(SYS_obtener_estado_del_enlace_mismo, (long)ruta, (long)memoria_intermedia_de_transferencia, 0, 0, 0, 0));
}

int obtener_estado_del_archivo_abierto(int descriptor_del_archivo, struct estado_del_archivo *memoria_intermedia_de_transferencia)
{
    return (int)__syscall_result(
        __syscall6(SYS_obtener_estado_del_archivo_abierto, descriptor_del_archivo, (long)memoria_intermedia_de_transferencia, 0, 0, 0, 0));
}

int obtener_información_del_sistema(struct utsname *identidad_del_sistema)
{
    return (int)__syscall_result(
        __syscall6(SYS_obtener_información_del_sistema, (long)identidad_del_sistema, 0, 0, 0, 0, 0));
}
