#include <Soubor_ABI.h>
#include <síť_ABI.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int podmínka, int vstupní_řádek) {
    검사항목수++;
    if (!podmínka) {
        puts("POSIX CHECK FAILED");
        char číslice_HODNOTA[12]; int délka_HODNOTA = 0;
        do { číslice_HODNOTA[délka_HODNOTA++] = '0' + vstupní_řádek % 10; vstupní_řádek /= 10; } while (vstupní_řádek);
        while (délka_HODNOTA) putchar(číslice_HODNOTA[--délka_HODNOTA]);
        putchar('\n'); _exit(1);
    }
}
#define ověřit(podmínka) 검사((podmínka), __LINE__)

int main(int 인수개수, char **argument_Seznam) {
    char data[32]; struct stat Stav_HODNOTA;
    ověřit(인수개수 == 2 && strcmp(argument_Seznam[1], "check") == 0 && argument_Seznam[2] == 0);
    ověřit(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ověřit(otevřít_Soubor("absent", jen_pro_čtení_HODNOTA) == -1 && číslo_chyby == ENOENT);
    int název_souboru = otevřít_Soubor("/posix.txt", pro_čtení_i_zápis | 새파일만들기, 0640);
    ověřit(název_souboru == 3);
    ověřit(zápis_Soubor_data(název_souboru, "abcd", 4) == 4);
    ověřit(otevřít_Soubor("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ověřit(파일상태읽기(název_souboru, &Stav_HODNOTA) == 0 && Stav_HODNOTA.st_size == 4 && S_ISREG(Stav_HODNOTA.st_mode));
    ověřit((Stav_HODNOTA.st_mode & 0777) == 0640 && Stav_HODNOTA.st_nlink == 1);
    ověřit(hledat_Soubor(název_souboru, 0, 처음기준) == 0);
    int klon_HODNOTA = duplikát_Soubor_popisovač(název_souboru);
    ověřit(klon_HODNOTA == 4);
    ověřit(파일자료읽기(klon_HODNOTA, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    ověřit(파일자료읽기(název_souboru, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    ověřit(파일자료읽기(název_souboru, data, 1) == 0);
    ověřit(fcntl(název_souboru, F_SETFD, FD_CLOEXEC) == 0 && fcntl(název_souboru, F_GETFD) == 1);
    ověřit(fcntl(klon_HODNOTA, F_GETFD) == 0);
    ověřit(dup2(název_souboru, název_souboru) == název_souboru && fcntl(název_souboru, F_GETFD) == 1);
    ověřit(dup2(-1, klon_HODNOTA) == -1 && errno == EBADF && fcntl(klon_HODNOTA, F_GETFD) == 0);
    ověřit(fcntl(klon_HODNOTA, F_SETFL, O_APPEND) == 0 && (fcntl(název_souboru, F_GETFL) & O_APPEND));
    ověřit(lseek(název_souboru, 0, SEEK_SET) == 0 && write(klon_HODNOTA, "e", 1) == 1 && lseek(název_souboru, 0, SEEK_CUR) == 5);
    ověřit(fcntl(název_souboru, F_SETFL, 0) == 0);
    ověřit(lseek(název_souboru, 8, SEEK_SET) == 8 && write(název_souboru, "Z", 1) == 1);
    ověřit(lseek(klon_HODNOTA, 5, SEEK_SET) == 5 && read(název_souboru, data, 4) == 4);
    ověřit(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    ověřit(ftruncate(název_souboru, 2) == 0 && lseek(název_souboru, 0, SEEK_CUR) == 9);
    ověřit(ftruncate(název_souboru, 6) == 0 && lseek(název_souboru, 2, SEEK_SET) == 2 && read(název_souboru, data, 4) == 4);
    ověřit(!data[0] && !data[1] && !data[2] && !data[3]);
    ověřit(lseek(název_souboru, 2147483647, SEEK_SET) == 2147483647);
    ověřit(lseek(název_souboru, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ověřit(lseek(název_souboru, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ověřit(write(název_souboru, "!", 1) == -1 && errno == EFBIG);
    ověřit(lseek(název_souboru, 0, SEEK_SET) == 0);
    ověřit(read(název_souboru, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ověřit(read(název_souboru, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ověřit(write(název_souboru, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ověřit(read(název_souboru, data, (size_t)-1) == -1 && errno == EINVAL);
    ověřit(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ověřit(fstat(název_souboru, (void *)0x00100000) == -1 && errno == EFAULT);
    ověřit(lseek(název_souboru, 0, SEEK_CUR) == 0);
    ověřit(read(název_souboru, NULL, 0) == 0 && write(název_souboru, NULL, 0) == 0);
    ověřit(odebrat_Soubor_položka_název("posix.txt") == 0);
    ověřit(fstat(název_souboru, &Stav_HODNOTA) == 0 && Stav_HODNOTA.st_nlink == 0 && Stav_HODNOTA.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ověřit(새파일 == 5 && fstat(새파일, &Stav_HODNOTA) == 0 && Stav_HODNOTA.st_size == 0);
    ověřit(read(název_souboru, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    ověřit(close(název_souboru) == 0 && close(klon_HODNOTA) == 0 && close(새파일) == 0);
    ověřit(close(새파일) == -1 && errno == EBADF);
    ověřit(unlink("posix.txt") == 0);
    název_souboru = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ověřit(název_souboru == 3 && fcntl(název_souboru, F_GETFD) == 1);
    ověřit(read(název_souboru, data, 1) == -1 && errno == EBADF);
    ověřit(write(název_souboru, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) ověřit(dup(název_souboru) == INDEX);
    ověřit(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ověřit(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ověřit(fstat(název_souboru, &Stav_HODNOTA) == 0 && Stav_HODNOTA.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) ověřit(close(INDEX) == 0);
    ověřit(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    název_souboru = open("posix.txt", O_RDONLY);
    ověřit(název_souboru == 3 && write(název_souboru, data, 1) == -1 && errno == EBADF);
    ověřit(fcntl(název_souboru, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ověřit(close(8) == 0 && close(název_souboru) == 0 && unlink("posix.txt") == 0);
    ověřit(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ověřit(fstat(1, &Stav_HODNOTA) == 0 && S_ISCHR(Stav_HODNOTA.st_mode));
    ověřit(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ověřit(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Adresa; char ODKAZ_SMS[16];
    ověřit(inet_pton(AF_INET, "10.0.2.2", &Adresa) == 1 && ntohl(Adresa.s_addr) == 0x0a000202U);
    ověřit(inet_ntop(AF_INET, &Adresa, ODKAZ_SMS, sizeof ODKAZ_SMS) == ODKAZ_SMS && strcmp(ODKAZ_SMS, "10.0.2.2") == 0);
    ověřit(inet_pton(AF_INET, "256.0.0.1", &Adresa) == 0 && ntohl(Adresa.s_addr) == 0x0a000202U);
    ověřit(inet_pton(AF_INET, "01.0.0.1", &Adresa) == 0);
    ověřit(inet_ntop(AF_INET, &Adresa, ODKAZ_SMS, 3) == NULL && errno == ENOSPC);
    ověřit(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], zboží_POČET = 0; char Název[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Název[4] = '0' + INDEX;
        int 열린파일 = open(Název, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ověřit(errno == ENOSPC); break; }
        보관[zboží_POČET++] = 열린파일;
    }
    ověřit(zboží_POČET > 0 && zboží_POČET < 8);
    ověřit(unlink("slot0") == 0);
    ověřit(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ověřit(close(보관[0]) == 0);
    název_souboru = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ověřit(název_souboru >= 0 && close(název_souboru) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < zboží_POČET; INDEX++) {
        Název[4] = '0' + INDEX;
        ověřit(close(보관[INDEX]) == 0 && unlink(Název) == 0);
    }
    ověřit(fsync(-1) == -1 && errno == EBADF);
    ověřit(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
