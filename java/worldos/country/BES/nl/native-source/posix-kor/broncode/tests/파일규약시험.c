#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int toestand, int invoerregel) {
    검사항목수++;
    if (!toestand) {
        puts("POSIX CHECK FAILED");
        char cijfer_WAARDE[12]; int tijdsduur_WAARDE = 0;
        do { cijfer_WAARDE[tijdsduur_WAARDE++] = '0' + invoerregel % 10; invoerregel /= 10; } while (invoerregel);
        while (tijdsduur_WAARDE) putchar(cijfer_WAARDE[--tijdsduur_WAARDE]);
        putchar('\n'); _exit(1);
    }
}
#define bevestigen(toestand) 검사((toestand), __LINE__)

int main(int 인수개수, char **argument_Lijst) {
    char gegevens[32]; struct stat Status_WAARDE;
    bevestigen(인수개수 == 2 && strcmp(argument_Lijst[1], "check") == 0 && argument_Lijst[2] == 0);
    bevestigen(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    bevestigen(open_Bestand("absent", alleen_lezen_WAARDE) == -1 && foutnummer == ENOENT);
    int bestand = open_Bestand("/posix.txt", lezen_schrijven | 새파일만들기, 0640);
    bevestigen(bestand == 3);
    bevestigen(schrijven_Bestand_gegevens(bestand, "abcd", 4) == 4);
    bevestigen(open_Bestand("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    bevestigen(파일상태읽기(bestand, &Status_WAARDE) == 0 && Status_WAARDE.st_size == 4 && S_ISREG(Status_WAARDE.st_mode));
    bevestigen((Status_WAARDE.st_mode & 0777) == 0640 && Status_WAARDE.st_nlink == 1);
    bevestigen(zoeken_Bestand(bestand, 0, 처음기준) == 0);
    int kloon_WAARDE = 파일서술자복제(bestand);
    bevestigen(kloon_WAARDE == 4);
    bevestigen(파일자료읽기(kloon_WAARDE, gegevens, 2) == 2 && memcmp(gegevens, "ab", 2) == 0);
    bevestigen(파일자료읽기(bestand, gegevens, 2) == 2 && memcmp(gegevens, "cd", 2) == 0);
    bevestigen(파일자료읽기(bestand, gegevens, 1) == 0);
    bevestigen(fcntl(bestand, F_SETFD, FD_CLOEXEC) == 0 && fcntl(bestand, F_GETFD) == 1);
    bevestigen(fcntl(kloon_WAARDE, F_GETFD) == 0);
    bevestigen(dup2(bestand, bestand) == bestand && fcntl(bestand, F_GETFD) == 1);
    bevestigen(dup2(-1, kloon_WAARDE) == -1 && errno == EBADF && fcntl(kloon_WAARDE, F_GETFD) == 0);
    bevestigen(fcntl(kloon_WAARDE, F_SETFL, O_APPEND) == 0 && (fcntl(bestand, F_GETFL) & O_APPEND));
    bevestigen(lseek(bestand, 0, SEEK_SET) == 0 && write(kloon_WAARDE, "e", 1) == 1 && lseek(bestand, 0, SEEK_CUR) == 5);
    bevestigen(fcntl(bestand, F_SETFL, 0) == 0);
    bevestigen(lseek(bestand, 8, SEEK_SET) == 8 && write(bestand, "Z", 1) == 1);
    bevestigen(lseek(kloon_WAARDE, 5, SEEK_SET) == 5 && read(bestand, gegevens, 4) == 4);
    bevestigen(gegevens[0] == 0 && gegevens[1] == 0 && gegevens[2] == 0 && gegevens[3] == 'Z');
    bevestigen(ftruncate(bestand, 2) == 0 && lseek(bestand, 0, SEEK_CUR) == 9);
    bevestigen(ftruncate(bestand, 6) == 0 && lseek(bestand, 2, SEEK_SET) == 2 && read(bestand, gegevens, 4) == 4);
    bevestigen(!gegevens[0] && !gegevens[1] && !gegevens[2] && !gegevens[3]);
    bevestigen(lseek(bestand, 2147483647, SEEK_SET) == 2147483647);
    bevestigen(lseek(bestand, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    bevestigen(lseek(bestand, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    bevestigen(write(bestand, "!", 1) == -1 && errno == EFBIG);
    bevestigen(lseek(bestand, 0, SEEK_SET) == 0);
    bevestigen(read(bestand, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    bevestigen(read(bestand, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    bevestigen(write(bestand, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    bevestigen(read(bestand, gegevens, (size_t)-1) == -1 && errno == EINVAL);
    bevestigen(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    bevestigen(fstat(bestand, (void *)0x00100000) == -1 && errno == EFAULT);
    bevestigen(lseek(bestand, 0, SEEK_CUR) == 0);
    bevestigen(read(bestand, NULL, 0) == 0 && write(bestand, NULL, 0) == 0);
    bevestigen(verwijderen_Bestand_invoer_naam("posix.txt") == 0);
    bevestigen(fstat(bestand, &Status_WAARDE) == 0 && Status_WAARDE.st_nlink == 0 && Status_WAARDE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    bevestigen(새파일 == 5 && fstat(새파일, &Status_WAARDE) == 0 && Status_WAARDE.st_size == 0);
    bevestigen(read(bestand, gegevens, 2) == 2 && memcmp(gegevens, "ab", 2) == 0);
    bevestigen(close(bestand) == 0 && close(kloon_WAARDE) == 0 && close(새파일) == 0);
    bevestigen(close(새파일) == -1 && errno == EBADF);
    bevestigen(unlink("posix.txt") == 0);
    bestand = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    bevestigen(bestand == 3 && fcntl(bestand, F_GETFD) == 1);
    bevestigen(read(bestand, gegevens, 1) == -1 && errno == EBADF);
    bevestigen(write(bestand, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) bevestigen(dup(bestand) == INDEX);
    bevestigen(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    bevestigen(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    bevestigen(fstat(bestand, &Status_WAARDE) == 0 && Status_WAARDE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) bevestigen(close(INDEX) == 0);
    bevestigen(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    bestand = open("posix.txt", O_RDONLY);
    bevestigen(bestand == 3 && write(bestand, gegevens, 1) == -1 && errno == EBADF);
    bevestigen(fcntl(bestand, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    bevestigen(close(8) == 0 && close(bestand) == 0 && unlink("posix.txt") == 0);
    bevestigen(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    bevestigen(fstat(1, &Status_WAARDE) == 0 && S_ISCHR(Status_WAARDE.st_mode));
    bevestigen(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    bevestigen(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADRES; char ADRES_sms[16];
    bevestigen(inet_pton(AF_INET, "10.0.2.2", &ADRES) == 1 && ntohl(ADRES.s_addr) == 0x0a000202U);
    bevestigen(inet_ntop(AF_INET, &ADRES, ADRES_sms, sizeof ADRES_sms) == ADRES_sms && strcmp(ADRES_sms, "10.0.2.2") == 0);
    bevestigen(inet_pton(AF_INET, "256.0.0.1", &ADRES) == 0 && ntohl(ADRES.s_addr) == 0x0a000202U);
    bevestigen(inet_pton(AF_INET, "01.0.0.1", &ADRES) == 0);
    bevestigen(inet_ntop(AF_INET, &ADRES, ADRES_sms, 3) == NULL && errno == ENOSPC);
    bevestigen(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], item_AANTAL = 0; char Naam[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Naam[4] = '0' + INDEX;
        int 열린파일 = open(Naam, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { bevestigen(errno == ENOSPC); break; }
        보관[item_AANTAL++] = 열린파일;
    }
    bevestigen(item_AANTAL > 0 && item_AANTAL < 8);
    bevestigen(unlink("slot0") == 0);
    bevestigen(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    bevestigen(close(보관[0]) == 0);
    bestand = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    bevestigen(bestand >= 0 && close(bestand) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < item_AANTAL; INDEX++) {
        Naam[4] = '0' + INDEX;
        bevestigen(close(보관[INDEX]) == 0 && unlink(Naam) == 0);
    }
    bevestigen(fsync(-1) == -1 && errno == EBADF);
    bevestigen(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
