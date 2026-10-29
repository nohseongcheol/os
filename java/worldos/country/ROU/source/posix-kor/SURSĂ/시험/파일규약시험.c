#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int condiție, int Linie) {
    검사항목수++;
    if (!condiție) {
        puts("POSIX CHECK FAILED");
        char cifră_VALUE[12]; int lungime_VALUE = 0;
        do { cifră_VALUE[lungime_VALUE++] = '0' + Linie % 10; Linie /= 10; } while (Linie);
        while (lungime_VALUE) putchar(cifră_VALUE[--lungime_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define verifica(condiție) 검사((condiție), __LINE__)

int main(int 인수개수, char **argument_Listă) {
    char date[32]; struct stat Stare_VALUE;
    verifica(인수개수 == 2 && strcmp(argument_Listă[1], "check") == 0 && argument_Listă[2] == 0);
    verifica(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verifica(crea_Fișier("absent", doar_în_citire_VALUE) == -1 && număr_de_eroare == ENOENT);
    int Fișier = crea_Fișier("/posix.txt", citire_scriere | 새파일만들기, 0640);
    verifica(Fișier == 3);
    verifica(scriere_Fișier_date(Fișier, "abcd", 4) == 4);
    verifica(crea_Fișier("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verifica(파일상태읽기(Fișier, &Stare_VALUE) == 0 && Stare_VALUE.st_size == 4 && S_ISREG(Stare_VALUE.st_mode));
    verifica((Stare_VALUE.st_mode & 0777) == 0640 && Stare_VALUE.st_nlink == 1);
    verifica(căuta_Fișier(Fișier, 0, 처음기준) == 0);
    int clona_VALUE = 파일서술자복제(Fișier);
    verifica(clona_VALUE == 4);
    verifica(파일자료읽기(clona_VALUE, date, 2) == 2 && memcmp(date, "ab", 2) == 0);
    verifica(파일자료읽기(Fișier, date, 2) == 2 && memcmp(date, "cd", 2) == 0);
    verifica(파일자료읽기(Fișier, date, 1) == 0);
    verifica(fcntl(Fișier, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fișier, F_GETFD) == 1);
    verifica(fcntl(clona_VALUE, F_GETFD) == 0);
    verifica(dup2(Fișier, Fișier) == Fișier && fcntl(Fișier, F_GETFD) == 1);
    verifica(dup2(-1, clona_VALUE) == -1 && errno == EBADF && fcntl(clona_VALUE, F_GETFD) == 0);
    verifica(fcntl(clona_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Fișier, F_GETFL) & O_APPEND));
    verifica(lseek(Fișier, 0, SEEK_SET) == 0 && write(clona_VALUE, "e", 1) == 1 && lseek(Fișier, 0, SEEK_CUR) == 5);
    verifica(fcntl(Fișier, F_SETFL, 0) == 0);
    verifica(lseek(Fișier, 8, SEEK_SET) == 8 && write(Fișier, "Z", 1) == 1);
    verifica(lseek(clona_VALUE, 5, SEEK_SET) == 5 && read(Fișier, date, 4) == 4);
    verifica(date[0] == 0 && date[1] == 0 && date[2] == 0 && date[3] == 'Z');
    verifica(ftruncate(Fișier, 2) == 0 && lseek(Fișier, 0, SEEK_CUR) == 9);
    verifica(ftruncate(Fișier, 6) == 0 && lseek(Fișier, 2, SEEK_SET) == 2 && read(Fișier, date, 4) == 4);
    verifica(!date[0] && !date[1] && !date[2] && !date[3]);
    verifica(lseek(Fișier, 2147483647, SEEK_SET) == 2147483647);
    verifica(lseek(Fișier, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verifica(lseek(Fișier, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verifica(write(Fișier, "!", 1) == -1 && errno == EFBIG);
    verifica(lseek(Fișier, 0, SEEK_SET) == 0);
    verifica(read(Fișier, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifica(read(Fișier, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verifica(write(Fișier, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifica(read(Fișier, date, (size_t)-1) == -1 && errno == EINVAL);
    verifica(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verifica(fstat(Fișier, (void *)0x00100000) == -1 && errno == EFAULT);
    verifica(lseek(Fișier, 0, SEEK_CUR) == 0);
    verifica(read(Fișier, NULL, 0) == 0 && write(Fișier, NULL, 0) == 0);
    verifica(elimina_Fișier_intrare_nume("posix.txt") == 0);
    verifica(fstat(Fișier, &Stare_VALUE) == 0 && Stare_VALUE.st_nlink == 0 && Stare_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifica(새파일 == 5 && fstat(새파일, &Stare_VALUE) == 0 && Stare_VALUE.st_size == 0);
    verifica(read(Fișier, date, 2) == 2 && memcmp(date, "ab", 2) == 0);
    verifica(close(Fișier) == 0 && close(clona_VALUE) == 0 && close(새파일) == 0);
    verifica(close(새파일) == -1 && errno == EBADF);
    verifica(unlink("posix.txt") == 0);
    Fișier = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verifica(Fișier == 3 && fcntl(Fișier, F_GETFD) == 1);
    verifica(read(Fișier, date, 1) == -1 && errno == EBADF);
    verifica(write(Fișier, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verifica(dup(Fișier) == INDEX);
    verifica(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verifica(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verifica(fstat(Fișier, &Stare_VALUE) == 0 && Stare_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verifica(close(INDEX) == 0);
    verifica(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fișier = open("posix.txt", O_RDONLY);
    verifica(Fișier == 3 && write(Fișier, date, 1) == -1 && errno == EBADF);
    verifica(fcntl(Fișier, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verifica(close(8) == 0 && close(Fișier) == 0 && unlink("posix.txt") == 0);
    verifica(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verifica(fstat(1, &Stare_VALUE) == 0 && S_ISCHR(Stare_VALUE.st_mode));
    verifica(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verifica(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresa; char adresa_SMS[16];
    verifica(inet_pton(AF_INET, "10.0.2.2", &adresa) == 1 && ntohl(adresa.s_addr) == 0x0a000202U);
    verifica(inet_ntop(AF_INET, &adresa, adresa_SMS, sizeof adresa_SMS) == adresa_SMS && strcmp(adresa_SMS, "10.0.2.2") == 0);
    verifica(inet_pton(AF_INET, "256.0.0.1", &adresa) == 0 && ntohl(adresa.s_addr) == 0x0a000202U);
    verifica(inet_pton(AF_INET, "01.0.0.1", &adresa) == 0);
    verifica(inet_ntop(AF_INET, &adresa, adresa_SMS, 3) == NULL && errno == ENOSPC);
    verifica(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], element_COUNT = 0; char Nume[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nume[4] = '0' + INDEX;
        int 열린파일 = open(Nume, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verifica(errno == ENOSPC); break; }
        보관[element_COUNT++] = 열린파일;
    }
    verifica(element_COUNT > 0 && element_COUNT < 8);
    verifica(unlink("slot0") == 0);
    verifica(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verifica(close(보관[0]) == 0);
    Fișier = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifica(Fișier >= 0 && close(Fișier) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < element_COUNT; INDEX++) {
        Nume[4] = '0' + INDEX;
        verifica(close(보관[INDEX]) == 0 && unlink(Nume) == 0);
    }
    verifica(fsync(-1) == -1 && errno == EBADF);
    verifica(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
