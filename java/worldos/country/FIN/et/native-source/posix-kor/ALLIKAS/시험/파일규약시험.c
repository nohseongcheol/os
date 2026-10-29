#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int tingimus, int Joon) {
    검사항목수++;
    if (!tingimus) {
        puts("POSIX CHECK FAILED");
        char number_VALUE[12]; int 길이 = 0;
        do { number_VALUE[길이++] = '0' + Joon % 10; Joon /= 10; } while (Joon);
        while (길이) putchar(number_VALUE[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define kinnitama(tingimus) 검사((tingimus), __LINE__)

int main(int 인수개수, char **argument_Loend) {
    char andmed[32]; struct stat Olek_VALUE;
    kinnitama(인수개수 == 2 && strcmp(argument_Loend[1], "check") == 0 && argument_Loend[2] == 0);
    kinnitama(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    kinnitama(avama_Fail("absent", kirjutuskaitstud_VALUE) == -1 && tõrke_number == ENOENT);
    int Fail = avama_Fail("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    kinnitama(Fail == 3);
    kinnitama(kirjutamine_Fail_andmed(Fail, "abcd", 4) == 4);
    kinnitama(avama_Fail("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    kinnitama(파일상태읽기(Fail, &Olek_VALUE) == 0 && Olek_VALUE.st_size == 4 && S_ISREG(Olek_VALUE.st_mode));
    kinnitama((Olek_VALUE.st_mode & 0777) == 0640 && Olek_VALUE.st_nlink == 1);
    kinnitama(otsima_Fail(Fail, 0, 처음기준) == 0);
    int kloon_VALUE = 파일서술자복제(Fail);
    kinnitama(kloon_VALUE == 4);
    kinnitama(파일자료읽기(kloon_VALUE, andmed, 2) == 2 && memcmp(andmed, "ab", 2) == 0);
    kinnitama(파일자료읽기(Fail, andmed, 2) == 2 && memcmp(andmed, "cd", 2) == 0);
    kinnitama(파일자료읽기(Fail, andmed, 1) == 0);
    kinnitama(fcntl(Fail, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fail, F_GETFD) == 1);
    kinnitama(fcntl(kloon_VALUE, F_GETFD) == 0);
    kinnitama(dup2(Fail, Fail) == Fail && fcntl(Fail, F_GETFD) == 1);
    kinnitama(dup2(-1, kloon_VALUE) == -1 && errno == EBADF && fcntl(kloon_VALUE, F_GETFD) == 0);
    kinnitama(fcntl(kloon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Fail, F_GETFL) & O_APPEND));
    kinnitama(lseek(Fail, 0, SEEK_SET) == 0 && write(kloon_VALUE, "e", 1) == 1 && lseek(Fail, 0, SEEK_CUR) == 5);
    kinnitama(fcntl(Fail, F_SETFL, 0) == 0);
    kinnitama(lseek(Fail, 8, SEEK_SET) == 8 && write(Fail, "Z", 1) == 1);
    kinnitama(lseek(kloon_VALUE, 5, SEEK_SET) == 5 && read(Fail, andmed, 4) == 4);
    kinnitama(andmed[0] == 0 && andmed[1] == 0 && andmed[2] == 0 && andmed[3] == 'Z');
    kinnitama(ftruncate(Fail, 2) == 0 && lseek(Fail, 0, SEEK_CUR) == 9);
    kinnitama(ftruncate(Fail, 6) == 0 && lseek(Fail, 2, SEEK_SET) == 2 && read(Fail, andmed, 4) == 4);
    kinnitama(!andmed[0] && !andmed[1] && !andmed[2] && !andmed[3]);
    kinnitama(lseek(Fail, 2147483647, SEEK_SET) == 2147483647);
    kinnitama(lseek(Fail, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    kinnitama(lseek(Fail, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    kinnitama(write(Fail, "!", 1) == -1 && errno == EFBIG);
    kinnitama(lseek(Fail, 0, SEEK_SET) == 0);
    kinnitama(read(Fail, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    kinnitama(read(Fail, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    kinnitama(write(Fail, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    kinnitama(read(Fail, andmed, (size_t)-1) == -1 && errno == EINVAL);
    kinnitama(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    kinnitama(fstat(Fail, (void *)0x00100000) == -1 && errno == EFAULT);
    kinnitama(lseek(Fail, 0, SEEK_CUR) == 0);
    kinnitama(read(Fail, NULL, 0) == 0 && write(Fail, NULL, 0) == 0);
    kinnitama(eemaldama_Fail_kirje_nimetus("posix.txt") == 0);
    kinnitama(fstat(Fail, &Olek_VALUE) == 0 && Olek_VALUE.st_nlink == 0 && Olek_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    kinnitama(새파일 == 5 && fstat(새파일, &Olek_VALUE) == 0 && Olek_VALUE.st_size == 0);
    kinnitama(read(Fail, andmed, 2) == 2 && memcmp(andmed, "ab", 2) == 0);
    kinnitama(close(Fail) == 0 && close(kloon_VALUE) == 0 && close(새파일) == 0);
    kinnitama(close(새파일) == -1 && errno == EBADF);
    kinnitama(unlink("posix.txt") == 0);
    Fail = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    kinnitama(Fail == 3 && fcntl(Fail, F_GETFD) == 1);
    kinnitama(read(Fail, andmed, 1) == -1 && errno == EBADF);
    kinnitama(write(Fail, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) kinnitama(dup(Fail) == INDEX);
    kinnitama(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    kinnitama(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    kinnitama(fstat(Fail, &Olek_VALUE) == 0 && Olek_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) kinnitama(close(INDEX) == 0);
    kinnitama(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fail = open("posix.txt", O_RDONLY);
    kinnitama(Fail == 3 && write(Fail, andmed, 1) == -1 && errno == EBADF);
    kinnitama(fcntl(Fail, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    kinnitama(close(8) == 0 && close(Fail) == 0 && unlink("posix.txt") == 0);
    kinnitama(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    kinnitama(fstat(1, &Olek_VALUE) == 0 && S_ISCHR(Olek_VALUE.st_mode));
    kinnitama(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    kinnitama(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    kinnitama(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    kinnitama(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    kinnitama(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    kinnitama(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    kinnitama(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    kinnitama(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], kaup_COUNT = 0; char Nimi_2[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nimi_2[4] = '0' + INDEX;
        int 열린파일 = open(Nimi_2, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { kinnitama(errno == ENOSPC); break; }
        보관[kaup_COUNT++] = 열린파일;
    }
    kinnitama(kaup_COUNT > 0 && kaup_COUNT < 8);
    kinnitama(unlink("slot0") == 0);
    kinnitama(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    kinnitama(close(보관[0]) == 0);
    Fail = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    kinnitama(Fail >= 0 && close(Fail) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < kaup_COUNT; INDEX++) {
        Nimi_2[4] = '0' + INDEX;
        kinnitama(close(보관[INDEX]) == 0 && unlink(Nimi_2) == 0);
    }
    kinnitama(fsync(-1) == -1 && errno == EBADF);
    kinnitama(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
