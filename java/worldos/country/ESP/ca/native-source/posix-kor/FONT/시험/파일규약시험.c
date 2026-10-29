#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int condició, int línia) {
    검사항목수++;
    if (!condició) {
        puts("POSIX CHECK FAILED");
        char dígit_VALOR[12]; int durada_VALOR = 0;
        do { dígit_VALOR[durada_VALOR++] = '0' + línia % 10; línia /= 10; } while (línia);
        while (durada_VALOR) putchar(dígit_VALOR[--durada_VALOR]);
        putchar('\n'); _exit(1);
    }
}
#define verificar(condició) 검사((condició), __LINE__)

int main(int 인수개수, char **arg_Llista) {
    char dades[32]; struct stat Estat_VALOR;
    verificar(인수개수 == 2 && strcmp(arg_Llista[1], "check") == 0 && arg_Llista[2] == 0);
    verificar(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verificar(crear_arxiu("absent", només_de_lectura_VALOR) == -1 && número_d_error == ENOENT);
    int Fitxer = crear_arxiu("/posix.txt", lectura_escriptura | 새파일만들기, 0640);
    verificar(Fitxer == 3);
    verificar(escriure_arxiu_dades(Fitxer, "abcd", 4) == 4);
    verificar(crear_arxiu("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verificar(tancar_arxiu_estat(Fitxer, &Estat_VALOR) == 0 && Estat_VALOR.st_size == 4 && S_ISREG(Estat_VALOR.st_mode));
    verificar((Estat_VALOR.st_mode & 0777) == 0640 && Estat_VALOR.st_nlink == 1);
    verificar(cercar_arxiu(Fitxer, 0, 처음기준) == 0);
    int clon_VALOR = 파일서술자복제(Fitxer);
    verificar(clon_VALOR == 4);
    verificar(tancar_arxiu_dades(clon_VALOR, dades, 2) == 2 && memcmp(dades, "ab", 2) == 0);
    verificar(tancar_arxiu_dades(Fitxer, dades, 2) == 2 && memcmp(dades, "cd", 2) == 0);
    verificar(tancar_arxiu_dades(Fitxer, dades, 1) == 0);
    verificar(fcntl(Fitxer, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fitxer, F_GETFD) == 1);
    verificar(fcntl(clon_VALOR, F_GETFD) == 0);
    verificar(dup2(Fitxer, Fitxer) == Fitxer && fcntl(Fitxer, F_GETFD) == 1);
    verificar(dup2(-1, clon_VALOR) == -1 && errno == EBADF && fcntl(clon_VALOR, F_GETFD) == 0);
    verificar(fcntl(clon_VALOR, F_SETFL, O_APPEND) == 0 && (fcntl(Fitxer, F_GETFL) & O_APPEND));
    verificar(lseek(Fitxer, 0, SEEK_SET) == 0 && write(clon_VALOR, "e", 1) == 1 && lseek(Fitxer, 0, SEEK_CUR) == 5);
    verificar(fcntl(Fitxer, F_SETFL, 0) == 0);
    verificar(lseek(Fitxer, 8, SEEK_SET) == 8 && write(Fitxer, "Z", 1) == 1);
    verificar(lseek(clon_VALOR, 5, SEEK_SET) == 5 && read(Fitxer, dades, 4) == 4);
    verificar(dades[0] == 0 && dades[1] == 0 && dades[2] == 0 && dades[3] == 'Z');
    verificar(ftruncate(Fitxer, 2) == 0 && lseek(Fitxer, 0, SEEK_CUR) == 9);
    verificar(ftruncate(Fitxer, 6) == 0 && lseek(Fitxer, 2, SEEK_SET) == 2 && read(Fitxer, dades, 4) == 4);
    verificar(!dades[0] && !dades[1] && !dades[2] && !dades[3]);
    verificar(lseek(Fitxer, 2147483647, SEEK_SET) == 2147483647);
    verificar(lseek(Fitxer, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verificar(lseek(Fitxer, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verificar(write(Fitxer, "!", 1) == -1 && errno == EFBIG);
    verificar(lseek(Fitxer, 0, SEEK_SET) == 0);
    verificar(read(Fitxer, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(Fitxer, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verificar(write(Fitxer, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(Fitxer, dades, (size_t)-1) == -1 && errno == EINVAL);
    verificar(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verificar(fstat(Fitxer, (void *)0x00100000) == -1 && errno == EFAULT);
    verificar(lseek(Fitxer, 0, SEEK_CUR) == 0);
    verificar(read(Fitxer, NULL, 0) == 0 && write(Fitxer, NULL, 0) == 0);
    verificar(suprimir_arxiu_introducció_nom("posix.txt") == 0);
    verificar(fstat(Fitxer, &Estat_VALOR) == 0 && Estat_VALOR.st_nlink == 0 && Estat_VALOR.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(새파일 == 5 && fstat(새파일, &Estat_VALOR) == 0 && Estat_VALOR.st_size == 0);
    verificar(read(Fitxer, dades, 2) == 2 && memcmp(dades, "ab", 2) == 0);
    verificar(close(Fitxer) == 0 && close(clon_VALOR) == 0 && close(새파일) == 0);
    verificar(close(새파일) == -1 && errno == EBADF);
    verificar(unlink("posix.txt") == 0);
    Fitxer = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verificar(Fitxer == 3 && fcntl(Fitxer, F_GETFD) == 1);
    verificar(read(Fitxer, dades, 1) == -1 && errno == EBADF);
    verificar(write(Fitxer, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verificar(dup(Fitxer) == INDEX);
    verificar(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verificar(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verificar(fstat(Fitxer, &Estat_VALOR) == 0 && Estat_VALOR.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verificar(close(INDEX) == 0);
    verificar(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fitxer = open("posix.txt", O_RDONLY);
    verificar(Fitxer == 3 && write(Fitxer, dades, 1) == -1 && errno == EBADF);
    verificar(fcntl(Fitxer, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verificar(close(8) == 0 && close(Fitxer) == 0 && unlink("posix.txt") == 0);
    verificar(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verificar(fstat(1, &Estat_VALOR) == 0 && S_ISCHR(Estat_VALOR.st_mode));
    verificar(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verificar(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Adreça; char ADREÇA_SMS[16];
    verificar(inet_pton(AF_INET, "10.0.2.2", &Adreça) == 1 && ntohl(Adreça.s_addr) == 0x0a000202U);
    verificar(inet_ntop(AF_INET, &Adreça, ADREÇA_SMS, sizeof ADREÇA_SMS) == ADREÇA_SMS && strcmp(ADREÇA_SMS, "10.0.2.2") == 0);
    verificar(inet_pton(AF_INET, "256.0.0.1", &Adreça) == 0 && ntohl(Adreça.s_addr) == 0x0a000202U);
    verificar(inet_pton(AF_INET, "01.0.0.1", &Adreça) == 0);
    verificar(inet_ntop(AF_INET, &Adreça, ADREÇA_SMS, 3) == NULL && errno == ENOSPC);
    verificar(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], element_COMPT = 0; char Nom[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nom[4] = '0' + INDEX;
        int 열린파일 = open(Nom, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verificar(errno == ENOSPC); break; }
        보관[element_COMPT++] = 열린파일;
    }
    verificar(element_COMPT > 0 && element_COMPT < 8);
    verificar(unlink("slot0") == 0);
    verificar(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verificar(close(보관[0]) == 0);
    Fitxer = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(Fitxer >= 0 && close(Fitxer) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < element_COMPT; INDEX++) {
        Nom[4] = '0' + INDEX;
        verificar(close(보관[INDEX]) == 0 && unlink(Nom) == 0);
    }
    verificar(fsync(-1) == -1 && errno == EBADF);
    verificar(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
