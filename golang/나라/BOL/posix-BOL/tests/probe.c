/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sistema/stat.h>
int __posix_library_test(void);

int main(void)
{
    char memoria_intermedia_de_transferencia_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    struct estado_del_archivo st;
    if (descriptor_del_archivo < 0 || obtener_estado_del_archivo_abierto(descriptor_del_archivo, &st) < 0 || leer(descriptor_del_archivo, memoria_intermedia_de_transferencia_2, 4) != 4 ||
        (unsigned char)memoria_intermedia_de_transferencia_2[0] != 0x7f || memoria_intermedia_de_transferencia_2[1] != 'E' || memoria_intermedia_de_transferencia_2[2] != 'L' || memoria_intermedia_de_transferencia_2[3] != 'F' ||
        mover_posición_del_archivo(descriptor_del_archivo, 0, SEEK_SET) != 0 || cerrar(descriptor_del_archivo) < 0 || obtener_identificador_de_proceso() <= 0)
        goto failure;
    errno = 0;
    if (leer(-1, memoria_intermedia_de_transferencia_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (escribir(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    escribir(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
