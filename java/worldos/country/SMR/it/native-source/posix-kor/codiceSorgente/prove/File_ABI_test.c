#include <File_ABI.h>
#include <rete_ABI.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int condizione, int riga_di_ingresso) {
    검사항목수++;
    if (!condizione) {
        puts("POSIX CHECK FAILED");
        char cifra_VALORE[12]; int durata_VALORE = 0;
        do { cifra_VALORE[durata_VALORE++] = '0' + riga_di_ingresso % 10; riga_di_ingresso /= 10; } while (riga_di_ingresso);
        while (durata_VALORE) putchar(cifra_VALORE[--durata_VALORE]);
        putchar('\n'); _exit(1);
    }
}
#define verificare(condizione) 검사((condizione), __LINE__)

int main(int 인수개수, char **argomento_elenco) {
    char dati[32]; struct stat Stato_VALORE;
    verificare(인수개수 == 2 && strcmp(argomento_elenco[1], "check") == 0 && argomento_elenco[2] == 0);
    verificare(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verificare(aperto_File("absent", di_sola_lettura_VALORE) == -1 && numero_errore == ENOENT);
    int file = aperto_File("/posix.txt", in_lettura_scrittura | 새파일만들기, 0640);
    verificare(file == 3);
    verificare(scrivere_File_dati(file, "abcd", 4) == 4);
    verificare(aperto_File("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verificare(파일상태읽기(file, &Stato_VALORE) == 0 && Stato_VALORE.st_size == 4 && S_ISREG(Stato_VALORE.st_mode));
    verificare((Stato_VALORE.st_mode & 0777) == 0640 && Stato_VALORE.st_nlink == 1);
    verificare(cercare_File(file, 0, 처음기준) == 0);
    int clone_VALORE = Duplica_File_descrittore(file);
    verificare(clone_VALORE == 4);
    verificare(파일자료읽기(clone_VALORE, dati, 2) == 2 && memcmp(dati, "ab", 2) == 0);
    verificare(파일자료읽기(file, dati, 2) == 2 && memcmp(dati, "cd", 2) == 0);
    verificare(파일자료읽기(file, dati, 1) == 0);
    verificare(fcntl(file, F_SETFD, FD_CLOEXEC) == 0 && fcntl(file, F_GETFD) == 1);
    verificare(fcntl(clone_VALORE, F_GETFD) == 0);
    verificare(dup2(file, file) == file && fcntl(file, F_GETFD) == 1);
    verificare(dup2(-1, clone_VALORE) == -1 && errno == EBADF && fcntl(clone_VALORE, F_GETFD) == 0);
    verificare(fcntl(clone_VALORE, F_SETFL, O_APPEND) == 0 && (fcntl(file, F_GETFL) & O_APPEND));
    verificare(lseek(file, 0, SEEK_SET) == 0 && write(clone_VALORE, "e", 1) == 1 && lseek(file, 0, SEEK_CUR) == 5);
    verificare(fcntl(file, F_SETFL, 0) == 0);
    verificare(lseek(file, 8, SEEK_SET) == 8 && write(file, "Z", 1) == 1);
    verificare(lseek(clone_VALORE, 5, SEEK_SET) == 5 && read(file, dati, 4) == 4);
    verificare(dati[0] == 0 && dati[1] == 0 && dati[2] == 0 && dati[3] == 'Z');
    verificare(ftruncate(file, 2) == 0 && lseek(file, 0, SEEK_CUR) == 9);
    verificare(ftruncate(file, 6) == 0 && lseek(file, 2, SEEK_SET) == 2 && read(file, dati, 4) == 4);
    verificare(!dati[0] && !dati[1] && !dati[2] && !dati[3]);
    verificare(lseek(file, 2147483647, SEEK_SET) == 2147483647);
    verificare(lseek(file, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verificare(lseek(file, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verificare(write(file, "!", 1) == -1 && errno == EFBIG);
    verificare(lseek(file, 0, SEEK_SET) == 0);
    verificare(read(file, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificare(read(file, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verificare(write(file, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificare(read(file, dati, (size_t)-1) == -1 && errno == EINVAL);
    verificare(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verificare(fstat(file, (void *)0x00100000) == -1 && errno == EFAULT);
    verificare(lseek(file, 0, SEEK_CUR) == 0);
    verificare(read(file, NULL, 0) == 0 && write(file, NULL, 0) == 0);
    verificare(rimuovere_File_voce_nome("posix.txt") == 0);
    verificare(fstat(file, &Stato_VALORE) == 0 && Stato_VALORE.st_nlink == 0 && Stato_VALORE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificare(새파일 == 5 && fstat(새파일, &Stato_VALORE) == 0 && Stato_VALORE.st_size == 0);
    verificare(read(file, dati, 2) == 2 && memcmp(dati, "ab", 2) == 0);
    verificare(close(file) == 0 && close(clone_VALORE) == 0 && close(새파일) == 0);
    verificare(close(새파일) == -1 && errno == EBADF);
    verificare(unlink("posix.txt") == 0);
    file = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verificare(file == 3 && fcntl(file, F_GETFD) == 1);
    verificare(read(file, dati, 1) == -1 && errno == EBADF);
    verificare(write(file, "keep", 4) == 4);
    for (int INDICE = 4; INDICE < 32; INDICE++) verificare(dup(file) == INDICE);
    verificare(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verificare(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verificare(fstat(file, &Stato_VALORE) == 0 && Stato_VALORE.st_size == 4);
    for (int INDICE = 3; INDICE < 32; INDICE++) verificare(close(INDICE) == 0);
    verificare(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    file = open("posix.txt", O_RDONLY);
    verificare(file == 3 && write(file, dati, 1) == -1 && errno == EBADF);
    verificare(fcntl(file, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verificare(close(8) == 0 && close(file) == 0 && unlink("posix.txt") == 0);
    verificare(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verificare(fstat(1, &Stato_VALORE) == 0 && S_ISCHR(Stato_VALORE.st_mode));
    verificare(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verificare(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr e_mail; char e_mail_SMS[16];
    verificare(inet_pton(AF_INET, "10.0.2.2", &e_mail) == 1 && ntohl(e_mail.s_addr) == 0x0a000202U);
    verificare(inet_ntop(AF_INET, &e_mail, e_mail_SMS, sizeof e_mail_SMS) == e_mail_SMS && strcmp(e_mail_SMS, "10.0.2.2") == 0);
    verificare(inet_pton(AF_INET, "256.0.0.1", &e_mail) == 0 && ntohl(e_mail.s_addr) == 0x0a000202U);
    verificare(inet_pton(AF_INET, "01.0.0.1", &e_mail) == 0);
    verificare(inet_ntop(AF_INET, &e_mail, e_mail_SMS, 3) == NULL && errno == ENOSPC);
    verificare(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], articolo_CONTA_NUMERI = 0; char Nome[] = "slot0";
    for (int INDICE = 0; INDICE < 8; INDICE++) {
        Nome[4] = '0' + INDICE;
        int 열린파일 = open(Nome, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verificare(errno == ENOSPC); break; }
        보관[articolo_CONTA_NUMERI++] = 열린파일;
    }
    verificare(articolo_CONTA_NUMERI > 0 && articolo_CONTA_NUMERI < 8);
    verificare(unlink("slot0") == 0);
    verificare(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verificare(close(보관[0]) == 0);
    file = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificare(file >= 0 && close(file) == 0 && unlink("held-slot") == 0);
    for (int INDICE = 1; INDICE < articolo_CONTA_NUMERI; INDICE++) {
        Nome[4] = '0' + INDICE;
        verificare(close(보관[INDICE]) == 0 && unlink(Nome) == 0);
    }
    verificare(fsync(-1) == -1 && errno == EBADF);
    verificare(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
