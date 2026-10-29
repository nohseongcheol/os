#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int condición, int Liña) {
    검사항목수++;
    if (!condición) {
        puts("POSIX CHECK FAILED");
        char díxito_VALOR[12]; int duración_VALOR = 0;
        do { díxito_VALOR[duración_VALOR++] = '0' + Liña % 10; Liña /= 10; } while (Liña);
        while (duración_VALOR) putchar(díxito_VALOR[--duración_VALOR]);
        putchar('\n'); _exit(1);
    }
}
#define verificar(condición) 검사((condición), __LINE__)

int main(int 인수개수, char **argumento_Lista) {
    char datos[32]; struct stat Estado_VALOR;
    verificar(인수개수 == 2 && strcmp(argumento_Lista[1], "check") == 0 && argumento_Lista[2] == 0);
    verificar(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verificar(abrir_Ficheiro("absent", só_de_lectura_VALOR) == -1 && número_de_erro == ENOENT);
    int Ficheiro = abrir_Ficheiro("/posix.txt", de_lectura_e_escrita | 새파일만들기, 0640);
    verificar(Ficheiro == 3);
    verificar(escribir_Ficheiro_datos(Ficheiro, "abcd", 4) == 4);
    verificar(abrir_Ficheiro("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verificar(파일상태읽기(Ficheiro, &Estado_VALOR) == 0 && Estado_VALOR.st_size == 4 && S_ISREG(Estado_VALOR.st_mode));
    verificar((Estado_VALOR.st_mode & 0777) == 0640 && Estado_VALOR.st_nlink == 1);
    verificar(buscar_Ficheiro(Ficheiro, 0, 처음기준) == 0);
    int clon_VALOR = 파일서술자복제(Ficheiro);
    verificar(clon_VALOR == 4);
    verificar(파일자료읽기(clon_VALOR, datos, 2) == 2 && memcmp(datos, "ab", 2) == 0);
    verificar(파일자료읽기(Ficheiro, datos, 2) == 2 && memcmp(datos, "cd", 2) == 0);
    verificar(파일자료읽기(Ficheiro, datos, 1) == 0);
    verificar(fcntl(Ficheiro, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Ficheiro, F_GETFD) == 1);
    verificar(fcntl(clon_VALOR, F_GETFD) == 0);
    verificar(dup2(Ficheiro, Ficheiro) == Ficheiro && fcntl(Ficheiro, F_GETFD) == 1);
    verificar(dup2(-1, clon_VALOR) == -1 && errno == EBADF && fcntl(clon_VALOR, F_GETFD) == 0);
    verificar(fcntl(clon_VALOR, F_SETFL, O_APPEND) == 0 && (fcntl(Ficheiro, F_GETFL) & O_APPEND));
    verificar(lseek(Ficheiro, 0, SEEK_SET) == 0 && write(clon_VALOR, "e", 1) == 1 && lseek(Ficheiro, 0, SEEK_CUR) == 5);
    verificar(fcntl(Ficheiro, F_SETFL, 0) == 0);
    verificar(lseek(Ficheiro, 8, SEEK_SET) == 8 && write(Ficheiro, "Z", 1) == 1);
    verificar(lseek(clon_VALOR, 5, SEEK_SET) == 5 && read(Ficheiro, datos, 4) == 4);
    verificar(datos[0] == 0 && datos[1] == 0 && datos[2] == 0 && datos[3] == 'Z');
    verificar(ftruncate(Ficheiro, 2) == 0 && lseek(Ficheiro, 0, SEEK_CUR) == 9);
    verificar(ftruncate(Ficheiro, 6) == 0 && lseek(Ficheiro, 2, SEEK_SET) == 2 && read(Ficheiro, datos, 4) == 4);
    verificar(!datos[0] && !datos[1] && !datos[2] && !datos[3]);
    verificar(lseek(Ficheiro, 2147483647, SEEK_SET) == 2147483647);
    verificar(lseek(Ficheiro, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verificar(lseek(Ficheiro, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verificar(write(Ficheiro, "!", 1) == -1 && errno == EFBIG);
    verificar(lseek(Ficheiro, 0, SEEK_SET) == 0);
    verificar(read(Ficheiro, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(Ficheiro, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verificar(write(Ficheiro, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(Ficheiro, datos, (size_t)-1) == -1 && errno == EINVAL);
    verificar(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verificar(fstat(Ficheiro, (void *)0x00100000) == -1 && errno == EFAULT);
    verificar(lseek(Ficheiro, 0, SEEK_CUR) == 0);
    verificar(read(Ficheiro, NULL, 0) == 0 && write(Ficheiro, NULL, 0) == 0);
    verificar(eliminar_Ficheiro_introdución_nome("posix.txt") == 0);
    verificar(fstat(Ficheiro, &Estado_VALOR) == 0 && Estado_VALOR.st_nlink == 0 && Estado_VALOR.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(새파일 == 5 && fstat(새파일, &Estado_VALOR) == 0 && Estado_VALOR.st_size == 0);
    verificar(read(Ficheiro, datos, 2) == 2 && memcmp(datos, "ab", 2) == 0);
    verificar(close(Ficheiro) == 0 && close(clon_VALOR) == 0 && close(새파일) == 0);
    verificar(close(새파일) == -1 && errno == EBADF);
    verificar(unlink("posix.txt") == 0);
    Ficheiro = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verificar(Ficheiro == 3 && fcntl(Ficheiro, F_GETFD) == 1);
    verificar(read(Ficheiro, datos, 1) == -1 && errno == EBADF);
    verificar(write(Ficheiro, "keep", 4) == 4);
    for (int ÍNDICE = 4; ÍNDICE < 32; ÍNDICE++) verificar(dup(Ficheiro) == ÍNDICE);
    verificar(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verificar(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verificar(fstat(Ficheiro, &Estado_VALOR) == 0 && Estado_VALOR.st_size == 4);
    for (int ÍNDICE = 3; ÍNDICE < 32; ÍNDICE++) verificar(close(ÍNDICE) == 0);
    verificar(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Ficheiro = open("posix.txt", O_RDONLY);
    verificar(Ficheiro == 3 && write(Ficheiro, datos, 1) == -1 && errno == EBADF);
    verificar(fcntl(Ficheiro, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verificar(close(8) == 0 && close(Ficheiro) == 0 && unlink("posix.txt") == 0);
    verificar(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verificar(fstat(1, &Estado_VALOR) == 0 && S_ISCHR(Estado_VALOR.st_mode));
    verificar(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verificar(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ENDEREZO; char ENDEREZO_SMS[16];
    verificar(inet_pton(AF_INET, "10.0.2.2", &ENDEREZO) == 1 && ntohl(ENDEREZO.s_addr) == 0x0a000202U);
    verificar(inet_ntop(AF_INET, &ENDEREZO, ENDEREZO_SMS, sizeof ENDEREZO_SMS) == ENDEREZO_SMS && strcmp(ENDEREZO_SMS, "10.0.2.2") == 0);
    verificar(inet_pton(AF_INET, "256.0.0.1", &ENDEREZO) == 0 && ntohl(ENDEREZO.s_addr) == 0x0a000202U);
    verificar(inet_pton(AF_INET, "01.0.0.1", &ENDEREZO) == 0);
    verificar(inet_ntop(AF_INET, &ENDEREZO, ENDEREZO_SMS, 3) == NULL && errno == ENOSPC);
    verificar(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], elemento_CONTAR = 0; char Nome[] = "slot0";
    for (int ÍNDICE = 0; ÍNDICE < 8; ÍNDICE++) {
        Nome[4] = '0' + ÍNDICE;
        int 열린파일 = open(Nome, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verificar(errno == ENOSPC); break; }
        보관[elemento_CONTAR++] = 열린파일;
    }
    verificar(elemento_CONTAR > 0 && elemento_CONTAR < 8);
    verificar(unlink("slot0") == 0);
    verificar(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verificar(close(보관[0]) == 0);
    Ficheiro = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(Ficheiro >= 0 && close(Ficheiro) == 0 && unlink("held-slot") == 0);
    for (int ÍNDICE = 1; ÍNDICE < elemento_CONTAR; ÍNDICE++) {
        Nome[4] = '0' + ÍNDICE;
        verificar(close(보관[ÍNDICE]) == 0 && unlink(Nome) == 0);
    }
    verificar(fsync(-1) == -1 && errno == EBADF);
    verificar(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
