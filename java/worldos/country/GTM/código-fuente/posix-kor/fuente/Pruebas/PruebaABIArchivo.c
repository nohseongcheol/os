#include <ABIArchivo.h>
#include <ABIRed.h>
#include <string.h>
#include <stdio.h>

static int númeroElementosElementoListaComprobado;
static void Comprobaciones(int condición, int línea) {
    númeroElementosElementoListaComprobado++;
    if (!condición) {
        puts("POSIX CHECK FAILED");
        char valorDígito[12]; int longitud = 0;
        do { valorDígito[longitud++] = '0' + línea % 10; línea /= 10; } while (línea);
        while (longitud) putchar(valorDígito[--longitud]);
        putchar('\n'); _exit(1);
    }
}
#define verificar(condición) Comprobaciones((condición), __LINE__)

int main(int númeroElementosArgumentos, char **listaArgumento) {
    char Datos[32]; struct stat valorEstadoValor;
    verificar(númeroElementosArgumentos == 2 && strcmp(listaArgumento[1], "check") == 0 && listaArgumento[2] == 0);
    verificar(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verificar(abrirArchivo("absent", leerValorSolamente) == -1 && númeroError == ENOENT);
    int Archivo = abrirArchivo("/posix.txt", EscribirLeer | crearArchivoNuevo, 0640);
    verificar(Archivo == 3);
    verificar(escribirDatosArchivo(Archivo, "abcd", 4) == 4);
    verificar(abrirArchivo("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verificar(leerEstadoArchivo(Archivo, &valorEstadoValor) == 0 && valorEstadoValor.st_size == 4 && S_ISREG(valorEstadoValor.st_mode));
    verificar((valorEstadoValor.st_mode & 0777) == 0640 && valorEstadoValor.st_nlink == 1);
    verificar(posicionarArchivo(Archivo, 0, PrincipioDesde) == 0);
    int valorClonar = descriptorArchivoDuplicado(Archivo);
    verificar(valorClonar == 4);
    verificar(leerDatosArchivo(valorClonar, Datos, 2) == 2 && memcmp(Datos, "ab", 2) == 0);
    verificar(leerDatosArchivo(Archivo, Datos, 2) == 2 && memcmp(Datos, "cd", 2) == 0);
    verificar(leerDatosArchivo(Archivo, Datos, 1) == 0);
    verificar(fcntl(Archivo, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Archivo, F_GETFD) == 1);
    verificar(fcntl(valorClonar, F_GETFD) == 0);
    verificar(dup2(Archivo, Archivo) == Archivo && fcntl(Archivo, F_GETFD) == 1);
    verificar(dup2(-1, valorClonar) == -1 && errno == EBADF && fcntl(valorClonar, F_GETFD) == 0);
    verificar(fcntl(valorClonar, F_SETFL, O_APPEND) == 0 && (fcntl(Archivo, F_GETFL) & O_APPEND));
    verificar(lseek(Archivo, 0, SEEK_SET) == 0 && write(valorClonar, "e", 1) == 1 && lseek(Archivo, 0, SEEK_CUR) == 5);
    verificar(fcntl(Archivo, F_SETFL, 0) == 0);
    verificar(lseek(Archivo, 8, SEEK_SET) == 8 && write(Archivo, "Z", 1) == 1);
    verificar(lseek(valorClonar, 5, SEEK_SET) == 5 && read(Archivo, Datos, 4) == 4);
    verificar(Datos[0] == 0 && Datos[1] == 0 && Datos[2] == 0 && Datos[3] == 'Z');
    verificar(ftruncate(Archivo, 2) == 0 && lseek(Archivo, 0, SEEK_CUR) == 9);
    verificar(ftruncate(Archivo, 6) == 0 && lseek(Archivo, 2, SEEK_SET) == 2 && read(Archivo, Datos, 4) == 4);
    verificar(!Datos[0] && !Datos[1] && !Datos[2] && !Datos[3]);
    verificar(lseek(Archivo, 2147483647, SEEK_SET) == 2147483647);
    verificar(lseek(Archivo, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verificar(lseek(Archivo, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verificar(write(Archivo, "!", 1) == -1 && errno == EFBIG);
    verificar(lseek(Archivo, 0, SEEK_SET) == 0);
    verificar(read(Archivo, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(Archivo, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verificar(write(Archivo, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(Archivo, Datos, (size_t)-1) == -1 && errno == EINVAL);
    verificar(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verificar(fstat(Archivo, (void *)0x00100000) == -1 && errno == EFAULT);
    verificar(lseek(Archivo, 0, SEEK_CUR) == 0);
    verificar(read(Archivo, NULL, 0) == 0 && write(Archivo, NULL, 0) == 0);
    verificar(eliminarNombreEntradaElementoArchivo("posix.txt") == 0);
    verificar(fstat(Archivo, &valorEstadoValor) == 0 && valorEstadoValor.st_nlink == 0 && valorEstadoValor.st_size == 6);
    int archivoNuevo = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(archivoNuevo == 5 && fstat(archivoNuevo, &valorEstadoValor) == 0 && valorEstadoValor.st_size == 0);
    verificar(read(Archivo, Datos, 2) == 2 && memcmp(Datos, "ab", 2) == 0);
    verificar(close(Archivo) == 0 && close(valorClonar) == 0 && close(archivoNuevo) == 0);
    verificar(close(archivoNuevo) == -1 && errno == EBADF);
    verificar(unlink("posix.txt") == 0);
    Archivo = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verificar(Archivo == 3 && fcntl(Archivo, F_GETFD) == 1);
    verificar(read(Archivo, Datos, 1) == -1 && errno == EBADF);
    verificar(write(Archivo, "keep", 4) == 4);
    for (int número = 4; número < 32; número++) verificar(dup(Archivo) == número);
    verificar(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verificar(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verificar(fstat(Archivo, &valorEstadoValor) == 0 && valorEstadoValor.st_size == 4);
    for (int número = 3; número < 32; número++) verificar(close(número) == 0);
    verificar(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Archivo = open("posix.txt", O_RDONLY);
    verificar(Archivo == 3 && write(Archivo, Datos, 1) == -1 && errno == EBADF);
    verificar(fcntl(Archivo, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verificar(close(8) == 0 && close(Archivo) == 0 && unlink("posix.txt") == 0);
    verificar(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verificar(fstat(1, &valorEstadoValor) == 0 && S_ISCHR(valorEstadoValor.st_mode));
    verificar(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verificar(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr dirección; char textoDirección[16];
    verificar(inet_pton(AF_INET, "10.0.2.2", &dirección) == 1 && ntohl(dirección.s_addr) == 0x0a000202U);
    verificar(inet_ntop(AF_INET, &dirección, textoDirección, sizeof textoDirección) == textoDirección && strcmp(textoDirección, "10.0.2.2") == 0);
    verificar(inet_pton(AF_INET, "256.0.0.1", &dirección) == 0 && ntohl(dirección.s_addr) == 0x0a000202U);
    verificar(inet_pton(AF_INET, "01.0.0.1", &dirección) == 0);
    verificar(inet_ntop(AF_INET, &dirección, textoDirección, 3) == NULL && errno == ENOSPC);
    verificar(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int preservarValor[8], númeroElementosElementoLista = 0; char nombre[] = "slot0";
    for (int número = 0; número < 8; número++) {
        nombre[4] = '0' + número;
        int archivoAbierto = open(nombre, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (archivoAbierto < 0) { verificar(errno == ENOSPC); break; }
        preservarValor[númeroElementosElementoLista++] = archivoAbierto;
    }
    verificar(númeroElementosElementoLista > 0 && númeroElementosElementoLista < 8);
    verificar(unlink("slot0") == 0);
    verificar(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verificar(close(preservarValor[0]) == 0);
    Archivo = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(Archivo >= 0 && close(Archivo) == 0 && unlink("held-slot") == 0);
    for (int número = 1; número < númeroElementosElementoLista; número++) {
        nombre[4] = '0' + número;
        verificar(close(preservarValor[número]) == 0 && unlink(nombre) == 0);
    }
    verificar(fsync(-1) == -1 && errno == EBADF);
    verificar(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
