#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int baldintza, int Marra) {
    검사항목수++;
    if (!baldintza) {
        puts("POSIX CHECK FAILED");
        char digitu_balio[12]; int luzera_balio = 0;
        do { digitu_balio[luzera_balio++] = '0' + Marra % 10; Marra /= 10; } while (Marra);
        while (luzera_balio) putchar(digitu_balio[--luzera_balio]);
        putchar('\n'); _exit(1);
    }
}
#define egiaztatu(baldintza) 검사((baldintza), __LINE__)

int main(int 인수개수, char **arg_Zerrenda) {
    char datuak[32]; struct stat Egoera_balio;
    egiaztatu(인수개수 == 2 && strcmp(arg_Zerrenda[1], "check") == 0 && arg_Zerrenda[2] == 0);
    egiaztatu(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    egiaztatu(ireki_fitxategi("absent", irakurtzeko_soilik_balio) == -1 && errorearen_zenbaki == ENOENT);
    int Fitxategia = ireki_fitxategi("/posix.txt", irakurri_idatzi | 새파일만들기, 0640);
    egiaztatu(Fitxategia == 3);
    egiaztatu(idatzi_fitxategi_datuak(Fitxategia, "abcd", 4) == 4);
    egiaztatu(ireki_fitxategi("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    egiaztatu(파일상태읽기(Fitxategia, &Egoera_balio) == 0 && Egoera_balio.st_size == 4 && S_ISREG(Egoera_balio.st_mode));
    egiaztatu((Egoera_balio.st_mode & 0777) == 0640 && Egoera_balio.st_nlink == 1);
    egiaztatu(bilatu_fitxategi(Fitxategia, 0, 처음기준) == 0);
    int klon_balio = 파일서술자복제(Fitxategia);
    egiaztatu(klon_balio == 4);
    egiaztatu(파일자료읽기(klon_balio, datuak, 2) == 2 && memcmp(datuak, "ab", 2) == 0);
    egiaztatu(파일자료읽기(Fitxategia, datuak, 2) == 2 && memcmp(datuak, "cd", 2) == 0);
    egiaztatu(파일자료읽기(Fitxategia, datuak, 1) == 0);
    egiaztatu(fcntl(Fitxategia, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fitxategia, F_GETFD) == 1);
    egiaztatu(fcntl(klon_balio, F_GETFD) == 0);
    egiaztatu(dup2(Fitxategia, Fitxategia) == Fitxategia && fcntl(Fitxategia, F_GETFD) == 1);
    egiaztatu(dup2(-1, klon_balio) == -1 && errno == EBADF && fcntl(klon_balio, F_GETFD) == 0);
    egiaztatu(fcntl(klon_balio, F_SETFL, O_APPEND) == 0 && (fcntl(Fitxategia, F_GETFL) & O_APPEND));
    egiaztatu(lseek(Fitxategia, 0, SEEK_SET) == 0 && write(klon_balio, "e", 1) == 1 && lseek(Fitxategia, 0, SEEK_CUR) == 5);
    egiaztatu(fcntl(Fitxategia, F_SETFL, 0) == 0);
    egiaztatu(lseek(Fitxategia, 8, SEEK_SET) == 8 && write(Fitxategia, "Z", 1) == 1);
    egiaztatu(lseek(klon_balio, 5, SEEK_SET) == 5 && read(Fitxategia, datuak, 4) == 4);
    egiaztatu(datuak[0] == 0 && datuak[1] == 0 && datuak[2] == 0 && datuak[3] == 'Z');
    egiaztatu(ftruncate(Fitxategia, 2) == 0 && lseek(Fitxategia, 0, SEEK_CUR) == 9);
    egiaztatu(ftruncate(Fitxategia, 6) == 0 && lseek(Fitxategia, 2, SEEK_SET) == 2 && read(Fitxategia, datuak, 4) == 4);
    egiaztatu(!datuak[0] && !datuak[1] && !datuak[2] && !datuak[3]);
    egiaztatu(lseek(Fitxategia, 2147483647, SEEK_SET) == 2147483647);
    egiaztatu(lseek(Fitxategia, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    egiaztatu(lseek(Fitxategia, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    egiaztatu(write(Fitxategia, "!", 1) == -1 && errno == EFBIG);
    egiaztatu(lseek(Fitxategia, 0, SEEK_SET) == 0);
    egiaztatu(read(Fitxategia, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    egiaztatu(read(Fitxategia, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    egiaztatu(write(Fitxategia, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    egiaztatu(read(Fitxategia, datuak, (size_t)-1) == -1 && errno == EINVAL);
    egiaztatu(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    egiaztatu(fstat(Fitxategia, (void *)0x00100000) == -1 && errno == EFAULT);
    egiaztatu(lseek(Fitxategia, 0, SEEK_CUR) == 0);
    egiaztatu(read(Fitxategia, NULL, 0) == 0 && write(Fitxategia, NULL, 0) == 0);
    egiaztatu(kendu_fitxategi_sarrera_izen("posix.txt") == 0);
    egiaztatu(fstat(Fitxategia, &Egoera_balio) == 0 && Egoera_balio.st_nlink == 0 && Egoera_balio.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    egiaztatu(새파일 == 5 && fstat(새파일, &Egoera_balio) == 0 && Egoera_balio.st_size == 0);
    egiaztatu(read(Fitxategia, datuak, 2) == 2 && memcmp(datuak, "ab", 2) == 0);
    egiaztatu(close(Fitxategia) == 0 && close(klon_balio) == 0 && close(새파일) == 0);
    egiaztatu(close(새파일) == -1 && errno == EBADF);
    egiaztatu(unlink("posix.txt") == 0);
    Fitxategia = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    egiaztatu(Fitxategia == 3 && fcntl(Fitxategia, F_GETFD) == 1);
    egiaztatu(read(Fitxategia, datuak, 1) == -1 && errno == EBADF);
    egiaztatu(write(Fitxategia, "keep", 4) == 4);
    for (int INDIZE = 4; INDIZE < 32; INDIZE++) egiaztatu(dup(Fitxategia) == INDIZE);
    egiaztatu(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    egiaztatu(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    egiaztatu(fstat(Fitxategia, &Egoera_balio) == 0 && Egoera_balio.st_size == 4);
    for (int INDIZE = 3; INDIZE < 32; INDIZE++) egiaztatu(close(INDIZE) == 0);
    egiaztatu(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fitxategia = open("posix.txt", O_RDONLY);
    egiaztatu(Fitxategia == 3 && write(Fitxategia, datuak, 1) == -1 && errno == EBADF);
    egiaztatu(fcntl(Fitxategia, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    egiaztatu(close(8) == 0 && close(Fitxategia) == 0 && unlink("posix.txt") == 0);
    egiaztatu(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    egiaztatu(fstat(1, &Egoera_balio) == 0 && S_ISCHR(Egoera_balio.st_mode));
    egiaztatu(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    egiaztatu(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr helbide; char helbide_SMS[16];
    egiaztatu(inet_pton(AF_INET, "10.0.2.2", &helbide) == 1 && ntohl(helbide.s_addr) == 0x0a000202U);
    egiaztatu(inet_ntop(AF_INET, &helbide, helbide_SMS, sizeof helbide_SMS) == helbide_SMS && strcmp(helbide_SMS, "10.0.2.2") == 0);
    egiaztatu(inet_pton(AF_INET, "256.0.0.1", &helbide) == 0 && ntohl(helbide.s_addr) == 0x0a000202U);
    egiaztatu(inet_pton(AF_INET, "01.0.0.1", &helbide) == 0);
    egiaztatu(inet_ntop(AF_INET, &helbide, helbide_SMS, 3) == NULL && errno == ENOSPC);
    egiaztatu(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], elementu_ZENBATU = 0; char Izena[] = "slot0";
    for (int INDIZE = 0; INDIZE < 8; INDIZE++) {
        Izena[4] = '0' + INDIZE;
        int 열린파일 = open(Izena, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { egiaztatu(errno == ENOSPC); break; }
        보관[elementu_ZENBATU++] = 열린파일;
    }
    egiaztatu(elementu_ZENBATU > 0 && elementu_ZENBATU < 8);
    egiaztatu(unlink("slot0") == 0);
    egiaztatu(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    egiaztatu(close(보관[0]) == 0);
    Fitxategia = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    egiaztatu(Fitxategia >= 0 && close(Fitxategia) == 0 && unlink("held-slot") == 0);
    for (int INDIZE = 1; INDIZE < elementu_ZENBATU; INDIZE++) {
        Izena[4] = '0' + INDIZE;
        egiaztatu(close(보관[INDIZE]) == 0 && unlink(Izena) == 0);
    }
    egiaztatu(fsync(-1) == -1 && errno == EBADF);
    egiaztatu(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
