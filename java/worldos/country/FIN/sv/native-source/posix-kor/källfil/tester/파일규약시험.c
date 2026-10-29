#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int villkor, int inmatningsrad) {
    검사항목수++;
    if (!villkor) {
        puts("POSIX CHECK FAILED");
        char siffra_värde[12]; int längd_värde = 0;
        do { siffra_värde[längd_värde++] = '0' + inmatningsrad % 10; inmatningsrad /= 10; } while (inmatningsrad);
        while (längd_värde) putchar(siffra_värde[--längd_värde]);
        putchar('\n'); _exit(1);
    }
}
#define verifiera(villkor) 검사((villkor), __LINE__)

int main(int 인수개수, char **argument_ange) {
    char data[32]; struct stat status_värde;
    verifiera(인수개수 == 2 && strcmp(argument_ange[1], "check") == 0 && argument_ange[2] == 0);
    verifiera(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verifiera(skapa_fil("absent", skrivskyddad_värde) == -1 && felnummer == ENOENT);
    int filnamn = skapa_fil("/posix.txt", läsa_skriva | 새파일만들기, 0640);
    verifiera(filnamn == 3);
    verifiera(skriva_fil_data(filnamn, "abcd", 4) == 4);
    verifiera(skapa_fil("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verifiera(läsa_fil_status(filnamn, &status_värde) == 0 && status_värde.st_size == 4 && S_ISREG(status_värde.st_mode));
    verifiera((status_värde.st_mode & 0777) == 0640 && status_värde.st_nlink == 1);
    verifiera(söka_fil(filnamn, 0, 처음기준) == 0);
    int klon_värde = 파일서술자복제(filnamn);
    verifiera(klon_värde == 4);
    verifiera(läsa_fil_data(klon_värde, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    verifiera(läsa_fil_data(filnamn, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    verifiera(läsa_fil_data(filnamn, data, 1) == 0);
    verifiera(fcntl(filnamn, F_SETFD, FD_CLOEXEC) == 0 && fcntl(filnamn, F_GETFD) == 1);
    verifiera(fcntl(klon_värde, F_GETFD) == 0);
    verifiera(dup2(filnamn, filnamn) == filnamn && fcntl(filnamn, F_GETFD) == 1);
    verifiera(dup2(-1, klon_värde) == -1 && errno == EBADF && fcntl(klon_värde, F_GETFD) == 0);
    verifiera(fcntl(klon_värde, F_SETFL, O_APPEND) == 0 && (fcntl(filnamn, F_GETFL) & O_APPEND));
    verifiera(lseek(filnamn, 0, SEEK_SET) == 0 && write(klon_värde, "e", 1) == 1 && lseek(filnamn, 0, SEEK_CUR) == 5);
    verifiera(fcntl(filnamn, F_SETFL, 0) == 0);
    verifiera(lseek(filnamn, 8, SEEK_SET) == 8 && write(filnamn, "Z", 1) == 1);
    verifiera(lseek(klon_värde, 5, SEEK_SET) == 5 && read(filnamn, data, 4) == 4);
    verifiera(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    verifiera(ftruncate(filnamn, 2) == 0 && lseek(filnamn, 0, SEEK_CUR) == 9);
    verifiera(ftruncate(filnamn, 6) == 0 && lseek(filnamn, 2, SEEK_SET) == 2 && read(filnamn, data, 4) == 4);
    verifiera(!data[0] && !data[1] && !data[2] && !data[3]);
    verifiera(lseek(filnamn, 2147483647, SEEK_SET) == 2147483647);
    verifiera(lseek(filnamn, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verifiera(lseek(filnamn, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verifiera(write(filnamn, "!", 1) == -1 && errno == EFBIG);
    verifiera(lseek(filnamn, 0, SEEK_SET) == 0);
    verifiera(read(filnamn, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifiera(read(filnamn, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verifiera(write(filnamn, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifiera(read(filnamn, data, (size_t)-1) == -1 && errno == EINVAL);
    verifiera(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verifiera(fstat(filnamn, (void *)0x00100000) == -1 && errno == EFAULT);
    verifiera(lseek(filnamn, 0, SEEK_CUR) == 0);
    verifiera(read(filnamn, NULL, 0) == 0 && write(filnamn, NULL, 0) == 0);
    verifiera(ta_bort_fil_post_namn("posix.txt") == 0);
    verifiera(fstat(filnamn, &status_värde) == 0 && status_värde.st_nlink == 0 && status_värde.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifiera(새파일 == 5 && fstat(새파일, &status_värde) == 0 && status_värde.st_size == 0);
    verifiera(read(filnamn, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    verifiera(close(filnamn) == 0 && close(klon_värde) == 0 && close(새파일) == 0);
    verifiera(close(새파일) == -1 && errno == EBADF);
    verifiera(unlink("posix.txt") == 0);
    filnamn = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verifiera(filnamn == 3 && fcntl(filnamn, F_GETFD) == 1);
    verifiera(read(filnamn, data, 1) == -1 && errno == EBADF);
    verifiera(write(filnamn, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verifiera(dup(filnamn) == INDEX);
    verifiera(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verifiera(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verifiera(fstat(filnamn, &status_värde) == 0 && status_värde.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verifiera(close(INDEX) == 0);
    verifiera(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    filnamn = open("posix.txt", O_RDONLY);
    verifiera(filnamn == 3 && write(filnamn, data, 1) == -1 && errno == EBADF);
    verifiera(fcntl(filnamn, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verifiera(close(8) == 0 && close(filnamn) == 0 && unlink("posix.txt") == 0);
    verifiera(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verifiera(fstat(1, &status_värde) == 0 && S_ISCHR(status_värde.st_mode));
    verifiera(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verifiera(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Adress; char ADRESS_SMS[16];
    verifiera(inet_pton(AF_INET, "10.0.2.2", &Adress) == 1 && ntohl(Adress.s_addr) == 0x0a000202U);
    verifiera(inet_ntop(AF_INET, &Adress, ADRESS_SMS, sizeof ADRESS_SMS) == ADRESS_SMS && strcmp(ADRESS_SMS, "10.0.2.2") == 0);
    verifiera(inet_pton(AF_INET, "256.0.0.1", &Adress) == 0 && ntohl(Adress.s_addr) == 0x0a000202U);
    verifiera(inet_pton(AF_INET, "01.0.0.1", &Adress) == 0);
    verifiera(inet_ntop(AF_INET, &Adress, ADRESS_SMS, 3) == NULL && errno == ENOSPC);
    verifiera(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], objekt_ANTAL = 0; char Namn[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Namn[4] = '0' + INDEX;
        int 열린파일 = open(Namn, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verifiera(errno == ENOSPC); break; }
        보관[objekt_ANTAL++] = 열린파일;
    }
    verifiera(objekt_ANTAL > 0 && objekt_ANTAL < 8);
    verifiera(unlink("slot0") == 0);
    verifiera(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verifiera(close(보관[0]) == 0);
    filnamn = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifiera(filnamn >= 0 && close(filnamn) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < objekt_ANTAL; INDEX++) {
        Namn[4] = '0' + INDEX;
        verifiera(close(보관[INDEX]) == 0 && unlink(Namn) == 0);
    }
    verifiera(fsync(-1) == -1 && errno == EBADF);
    verifiera(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
