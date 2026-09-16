/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sistema/stat.h>
#include <sistema/identidad_del_sistema.h>
#include <sistema/espera_de_hijos.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct estado_del_archivo st;
    struct utsname identidad_del_sistema;
    int descriptor_del_archivo = abrir("/USER1", O_RDONLY);
    int copy = descriptor_del_archivo >= 0 ? duplicar_referencia_de_archivo_abierto(descriptor_del_archivo) : -1;
    if (copy >= 0) cerrar(copy);
    if (descriptor_del_archivo >= 0) {
        obtener_estado_del_archivo_abierto(descriptor_del_archivo, &st);
        mover_posición_del_archivo(descriptor_del_archivo, 0, SEEK_SET);
        cerrar(descriptor_del_archivo);
    }
    estado_del_archivo("/", &st);
    obtener_información_del_sistema(&identidad_del_sistema);
    obtener_ruta_del_directorio_de_trabajo(cwd, sizeof(cwd));
    return errno + obtener_identificador_de_proceso() + obtener_identificador_del_padre();
}
