#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int tilstand, int linje) {
    검사항목수++;
    if (!tilstand) {
        puts("POSIX CHECK FAILED");
        char siffer_VALUE[12]; int lengd_VALUE = 0;
        do { siffer_VALUE[lengd_VALUE++] = '0' + linje % 10; linje /= 10; } while (linje);
        while (lengd_VALUE) putchar(siffer_VALUE[--lengd_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define stadfeste(tilstand) 검사((tilstand), __LINE__)

int main(int 인수개수, char **argument_Liste) {
    char data[32]; struct stat status_VALUE;
    stadfeste(인수개수 == 2 && strcmp(argument_Liste[1], "check") == 0 && argument_Liste[2] == 0);
    stadfeste(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    stadfeste(opne_fil("absent", skriveverna_VALUE) == -1 && feilnummer == ENOENT);
    int Fil = opne_fil("/posix.txt", lese_og_skrivetilgang | 새파일만들기, 0640);
    stadfeste(Fil == 3);
    stadfeste(skrive_fil_data(Fil, "abcd", 4) == 4);
    stadfeste(opne_fil("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    stadfeste(파일상태읽기(Fil, &status_VALUE) == 0 && status_VALUE.st_size == 4 && S_ISREG(status_VALUE.st_mode));
    stadfeste((status_VALUE.st_mode & 0777) == 0640 && status_VALUE.st_nlink == 1);
    stadfeste(søk_fil(Fil, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Fil);
    stadfeste(복제 == 4);
    stadfeste(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    stadfeste(파일자료읽기(Fil, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    stadfeste(파일자료읽기(Fil, data, 1) == 0);
    stadfeste(fcntl(Fil, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fil, F_GETFD) == 1);
    stadfeste(fcntl(복제, F_GETFD) == 0);
    stadfeste(dup2(Fil, Fil) == Fil && fcntl(Fil, F_GETFD) == 1);
    stadfeste(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    stadfeste(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Fil, F_GETFL) & O_APPEND));
    stadfeste(lseek(Fil, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Fil, 0, SEEK_CUR) == 5);
    stadfeste(fcntl(Fil, F_SETFL, 0) == 0);
    stadfeste(lseek(Fil, 8, SEEK_SET) == 8 && write(Fil, "Z", 1) == 1);
    stadfeste(lseek(복제, 5, SEEK_SET) == 5 && read(Fil, data, 4) == 4);
    stadfeste(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    stadfeste(ftruncate(Fil, 2) == 0 && lseek(Fil, 0, SEEK_CUR) == 9);
    stadfeste(ftruncate(Fil, 6) == 0 && lseek(Fil, 2, SEEK_SET) == 2 && read(Fil, data, 4) == 4);
    stadfeste(!data[0] && !data[1] && !data[2] && !data[3]);
    stadfeste(lseek(Fil, 2147483647, SEEK_SET) == 2147483647);
    stadfeste(lseek(Fil, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    stadfeste(lseek(Fil, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    stadfeste(write(Fil, "!", 1) == -1 && errno == EFBIG);
    stadfeste(lseek(Fil, 0, SEEK_SET) == 0);
    stadfeste(read(Fil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    stadfeste(read(Fil, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    stadfeste(write(Fil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    stadfeste(read(Fil, data, (size_t)-1) == -1 && errno == EINVAL);
    stadfeste(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    stadfeste(fstat(Fil, (void *)0x00100000) == -1 && errno == EFAULT);
    stadfeste(lseek(Fil, 0, SEEK_CUR) == 0);
    stadfeste(read(Fil, NULL, 0) == 0 && write(Fil, NULL, 0) == 0);
    stadfeste(fjerne_fil_oppføring_namn("posix.txt") == 0);
    stadfeste(fstat(Fil, &status_VALUE) == 0 && status_VALUE.st_nlink == 0 && status_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    stadfeste(새파일 == 5 && fstat(새파일, &status_VALUE) == 0 && status_VALUE.st_size == 0);
    stadfeste(read(Fil, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    stadfeste(close(Fil) == 0 && close(복제) == 0 && close(새파일) == 0);
    stadfeste(close(새파일) == -1 && errno == EBADF);
    stadfeste(unlink("posix.txt") == 0);
    Fil = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    stadfeste(Fil == 3 && fcntl(Fil, F_GETFD) == 1);
    stadfeste(read(Fil, data, 1) == -1 && errno == EBADF);
    stadfeste(write(Fil, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) stadfeste(dup(Fil) == INDEX);
    stadfeste(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    stadfeste(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    stadfeste(fstat(Fil, &status_VALUE) == 0 && status_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) stadfeste(close(INDEX) == 0);
    stadfeste(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fil = open("posix.txt", O_RDONLY);
    stadfeste(Fil == 3 && write(Fil, data, 1) == -1 && errno == EBADF);
    stadfeste(fcntl(Fil, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    stadfeste(close(8) == 0 && close(Fil) == 0 && unlink("posix.txt") == 0);
    stadfeste(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    stadfeste(fstat(1, &status_VALUE) == 0 && S_ISCHR(status_VALUE.st_mode));
    stadfeste(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    stadfeste(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    stadfeste(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    stadfeste(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    stadfeste(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    stadfeste(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    stadfeste(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    stadfeste(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], vare_COUNT = 0; char Namn[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Namn[4] = '0' + INDEX;
        int 열린파일 = open(Namn, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { stadfeste(errno == ENOSPC); break; }
        보관[vare_COUNT++] = 열린파일;
    }
    stadfeste(vare_COUNT > 0 && vare_COUNT < 8);
    stadfeste(unlink("slot0") == 0);
    stadfeste(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    stadfeste(close(보관[0]) == 0);
    Fil = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    stadfeste(Fil >= 0 && close(Fil) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < vare_COUNT; INDEX++) {
        Namn[4] = '0' + INDEX;
        stadfeste(close(보관[INDEX]) == 0 && unlink(Namn) == 0);
    }
    stadfeste(fsync(-1) == -1 && errno == EBADF);
    stadfeste(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
