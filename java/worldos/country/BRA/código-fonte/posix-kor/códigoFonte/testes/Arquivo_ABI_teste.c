#include <Arquivo_ABI.h>
#include <rede_ABI.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int doença, int linha_de_entrada) {
    검사항목수++;
    if (!doença) {
        puts("POSIX CHECK FAILED");
        char dígito_VALOR[12]; int duração_VALOR = 0;
        do { dígito_VALOR[duração_VALOR++] = '0' + linha_de_entrada % 10; linha_de_entrada /= 10; } while (linha_de_entrada);
        while (duração_VALOR) putchar(dígito_VALOR[--duração_VALOR]);
        putchar('\n'); _exit(1);
    }
}
#define verificar(doença) 검사((doença), __LINE__)

int main(int 인수개수, char **argumento_Lista) {
    char dados[32]; struct stat Estado_VALOR;
    verificar(인수개수 == 2 && strcmp(argumento_Lista[1], "check") == 0 && argumento_Lista[2] == 0);
    verificar(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verificar(abrir_Arquivo("absent", somente_leitura_VALOR) == -1 && número_do_erro == ENOENT);
    int ficheiro = abrir_Arquivo("/posix.txt", de_leitura_gravação | 새파일만들기, 0640);
    verificar(ficheiro == 3);
    verificar(gravar_Arquivo_dados(ficheiro, "abcd", 4) == 4);
    verificar(abrir_Arquivo("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verificar(leitura_Arquivo_Status(ficheiro, &Estado_VALOR) == 0 && Estado_VALOR.st_size == 4 && S_ISREG(Estado_VALOR.st_mode));
    verificar((Estado_VALOR.st_mode & 0777) == 0640 && Estado_VALOR.st_nlink == 1);
    verificar(busca_Arquivo(ficheiro, 0, 처음기준) == 0);
    int clone_VALOR = Duplicar_Arquivo_descritor(ficheiro);
    verificar(clone_VALOR == 4);
    verificar(leitura_Arquivo_dados(clone_VALOR, dados, 2) == 2 && memcmp(dados, "ab", 2) == 0);
    verificar(leitura_Arquivo_dados(ficheiro, dados, 2) == 2 && memcmp(dados, "cd", 2) == 0);
    verificar(leitura_Arquivo_dados(ficheiro, dados, 1) == 0);
    verificar(fcntl(ficheiro, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ficheiro, F_GETFD) == 1);
    verificar(fcntl(clone_VALOR, F_GETFD) == 0);
    verificar(dup2(ficheiro, ficheiro) == ficheiro && fcntl(ficheiro, F_GETFD) == 1);
    verificar(dup2(-1, clone_VALOR) == -1 && errno == EBADF && fcntl(clone_VALOR, F_GETFD) == 0);
    verificar(fcntl(clone_VALOR, F_SETFL, O_APPEND) == 0 && (fcntl(ficheiro, F_GETFL) & O_APPEND));
    verificar(lseek(ficheiro, 0, SEEK_SET) == 0 && write(clone_VALOR, "e", 1) == 1 && lseek(ficheiro, 0, SEEK_CUR) == 5);
    verificar(fcntl(ficheiro, F_SETFL, 0) == 0);
    verificar(lseek(ficheiro, 8, SEEK_SET) == 8 && write(ficheiro, "Z", 1) == 1);
    verificar(lseek(clone_VALOR, 5, SEEK_SET) == 5 && read(ficheiro, dados, 4) == 4);
    verificar(dados[0] == 0 && dados[1] == 0 && dados[2] == 0 && dados[3] == 'Z');
    verificar(ftruncate(ficheiro, 2) == 0 && lseek(ficheiro, 0, SEEK_CUR) == 9);
    verificar(ftruncate(ficheiro, 6) == 0 && lseek(ficheiro, 2, SEEK_SET) == 2 && read(ficheiro, dados, 4) == 4);
    verificar(!dados[0] && !dados[1] && !dados[2] && !dados[3]);
    verificar(lseek(ficheiro, 2147483647, SEEK_SET) == 2147483647);
    verificar(lseek(ficheiro, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verificar(lseek(ficheiro, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verificar(write(ficheiro, "!", 1) == -1 && errno == EFBIG);
    verificar(lseek(ficheiro, 0, SEEK_SET) == 0);
    verificar(read(ficheiro, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(ficheiro, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verificar(write(ficheiro, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificar(read(ficheiro, dados, (size_t)-1) == -1 && errno == EINVAL);
    verificar(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verificar(fstat(ficheiro, (void *)0x00100000) == -1 && errno == EFAULT);
    verificar(lseek(ficheiro, 0, SEEK_CUR) == 0);
    verificar(read(ficheiro, NULL, 0) == 0 && write(ficheiro, NULL, 0) == 0);
    verificar(remover_Arquivo_entrada_nome("posix.txt") == 0);
    verificar(fstat(ficheiro, &Estado_VALOR) == 0 && Estado_VALOR.st_nlink == 0 && Estado_VALOR.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(새파일 == 5 && fstat(새파일, &Estado_VALOR) == 0 && Estado_VALOR.st_size == 0);
    verificar(read(ficheiro, dados, 2) == 2 && memcmp(dados, "ab", 2) == 0);
    verificar(close(ficheiro) == 0 && close(clone_VALOR) == 0 && close(새파일) == 0);
    verificar(close(새파일) == -1 && errno == EBADF);
    verificar(unlink("posix.txt") == 0);
    ficheiro = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verificar(ficheiro == 3 && fcntl(ficheiro, F_GETFD) == 1);
    verificar(read(ficheiro, dados, 1) == -1 && errno == EBADF);
    verificar(write(ficheiro, "keep", 4) == 4);
    for (int ÍNDICE = 4; ÍNDICE < 32; ÍNDICE++) verificar(dup(ficheiro) == ÍNDICE);
    verificar(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verificar(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verificar(fstat(ficheiro, &Estado_VALOR) == 0 && Estado_VALOR.st_size == 4);
    for (int ÍNDICE = 3; ÍNDICE < 32; ÍNDICE++) verificar(close(ÍNDICE) == 0);
    verificar(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ficheiro = open("posix.txt", O_RDONLY);
    verificar(ficheiro == 3 && write(ficheiro, dados, 1) == -1 && errno == EBADF);
    verificar(fcntl(ficheiro, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verificar(close(8) == 0 && close(ficheiro) == 0 && unlink("posix.txt") == 0);
    verificar(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verificar(fstat(1, &Estado_VALOR) == 0 && S_ISCHR(Estado_VALOR.st_mode));
    verificar(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verificar(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Endereço; char email_SMS[16];
    verificar(inet_pton(AF_INET, "10.0.2.2", &Endereço) == 1 && ntohl(Endereço.s_addr) == 0x0a000202U);
    verificar(inet_ntop(AF_INET, &Endereço, email_SMS, sizeof email_SMS) == email_SMS && strcmp(email_SMS, "10.0.2.2") == 0);
    verificar(inet_pton(AF_INET, "256.0.0.1", &Endereço) == 0 && ntohl(Endereço.s_addr) == 0x0a000202U);
    verificar(inet_pton(AF_INET, "01.0.0.1", &Endereço) == 0);
    verificar(inet_ntop(AF_INET, &Endereço, email_SMS, 3) == NULL && errno == ENOSPC);
    verificar(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], item_CONT_NÚM = 0; char Nome[] = "slot0";
    for (int ÍNDICE = 0; ÍNDICE < 8; ÍNDICE++) {
        Nome[4] = '0' + ÍNDICE;
        int 열린파일 = open(Nome, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verificar(errno == ENOSPC); break; }
        보관[item_CONT_NÚM++] = 열린파일;
    }
    verificar(item_CONT_NÚM > 0 && item_CONT_NÚM < 8);
    verificar(unlink("slot0") == 0);
    verificar(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verificar(close(보관[0]) == 0);
    ficheiro = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificar(ficheiro >= 0 && close(ficheiro) == 0 && unlink("held-slot") == 0);
    for (int ÍNDICE = 1; ÍNDICE < item_CONT_NÚM; ÍNDICE++) {
        Nome[4] = '0' + ÍNDICE;
        verificar(close(보관[ÍNDICE]) == 0 && unlink(Nome) == 0);
    }
    verificar(fsync(-1) == -1 && errno == EBADF);
    verificar(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
