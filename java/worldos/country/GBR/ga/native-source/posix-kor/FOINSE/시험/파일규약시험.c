#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int coinníoll, int Líne) {
    검사항목수++;
    if (!coinníoll) {
        puts("POSIX CHECK FAILED");
        char digit_VALUE[12]; int fad_VALUE = 0;
        do { digit_VALUE[fad_VALUE++] = '0' + Líne % 10; Líne /= 10; } while (Líne);
        while (fad_VALUE) putchar(digit_VALUE[--fad_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define fíoraigh(coinníoll) 검사((coinníoll), __LINE__)

int main(int 인수개수, char **argóint_Liosta) {
    char sonraí[32]; struct stat staid_VALUE;
    fíoraigh(인수개수 == 2 && strcmp(argóint_Liosta[1], "check") == 0 && argóint_Liosta[2] == 0);
    fíoraigh(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    fíoraigh(oscail_comhad("absent", inléite_amháin_VALUE) == -1 && 오류번호 == ENOENT);
    int Comhad = oscail_comhad("/posix.txt", inléite_inscríofa | 새파일만들기, 0640);
    fíoraigh(Comhad == 3);
    fíoraigh(scríobh_comhad_sonraí(Comhad, "abcd", 4) == 4);
    fíoraigh(oscail_comhad("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    fíoraigh(파일상태읽기(Comhad, &staid_VALUE) == 0 && staid_VALUE.st_size == 4 && S_ISREG(staid_VALUE.st_mode));
    fíoraigh((staid_VALUE.st_mode & 0777) == 0640 && staid_VALUE.st_nlink == 1);
    fíoraigh(lorg_comhad(Comhad, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Comhad);
    fíoraigh(복제 == 4);
    fíoraigh(파일자료읽기(복제, sonraí, 2) == 2 && memcmp(sonraí, "ab", 2) == 0);
    fíoraigh(파일자료읽기(Comhad, sonraí, 2) == 2 && memcmp(sonraí, "cd", 2) == 0);
    fíoraigh(파일자료읽기(Comhad, sonraí, 1) == 0);
    fíoraigh(fcntl(Comhad, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Comhad, F_GETFD) == 1);
    fíoraigh(fcntl(복제, F_GETFD) == 0);
    fíoraigh(dup2(Comhad, Comhad) == Comhad && fcntl(Comhad, F_GETFD) == 1);
    fíoraigh(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    fíoraigh(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Comhad, F_GETFL) & O_APPEND));
    fíoraigh(lseek(Comhad, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Comhad, 0, SEEK_CUR) == 5);
    fíoraigh(fcntl(Comhad, F_SETFL, 0) == 0);
    fíoraigh(lseek(Comhad, 8, SEEK_SET) == 8 && write(Comhad, "Z", 1) == 1);
    fíoraigh(lseek(복제, 5, SEEK_SET) == 5 && read(Comhad, sonraí, 4) == 4);
    fíoraigh(sonraí[0] == 0 && sonraí[1] == 0 && sonraí[2] == 0 && sonraí[3] == 'Z');
    fíoraigh(ftruncate(Comhad, 2) == 0 && lseek(Comhad, 0, SEEK_CUR) == 9);
    fíoraigh(ftruncate(Comhad, 6) == 0 && lseek(Comhad, 2, SEEK_SET) == 2 && read(Comhad, sonraí, 4) == 4);
    fíoraigh(!sonraí[0] && !sonraí[1] && !sonraí[2] && !sonraí[3]);
    fíoraigh(lseek(Comhad, 2147483647, SEEK_SET) == 2147483647);
    fíoraigh(lseek(Comhad, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    fíoraigh(lseek(Comhad, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    fíoraigh(write(Comhad, "!", 1) == -1 && errno == EFBIG);
    fíoraigh(lseek(Comhad, 0, SEEK_SET) == 0);
    fíoraigh(read(Comhad, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    fíoraigh(read(Comhad, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    fíoraigh(write(Comhad, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    fíoraigh(read(Comhad, sonraí, (size_t)-1) == -1 && errno == EINVAL);
    fíoraigh(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    fíoraigh(fstat(Comhad, (void *)0x00100000) == -1 && errno == EFAULT);
    fíoraigh(lseek(Comhad, 0, SEEK_CUR) == 0);
    fíoraigh(read(Comhad, NULL, 0) == 0 && write(Comhad, NULL, 0) == 0);
    fíoraigh(bain_comhad_iontráil_ainm("posix.txt") == 0);
    fíoraigh(fstat(Comhad, &staid_VALUE) == 0 && staid_VALUE.st_nlink == 0 && staid_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    fíoraigh(새파일 == 5 && fstat(새파일, &staid_VALUE) == 0 && staid_VALUE.st_size == 0);
    fíoraigh(read(Comhad, sonraí, 2) == 2 && memcmp(sonraí, "ab", 2) == 0);
    fíoraigh(close(Comhad) == 0 && close(복제) == 0 && close(새파일) == 0);
    fíoraigh(close(새파일) == -1 && errno == EBADF);
    fíoraigh(unlink("posix.txt") == 0);
    Comhad = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    fíoraigh(Comhad == 3 && fcntl(Comhad, F_GETFD) == 1);
    fíoraigh(read(Comhad, sonraí, 1) == -1 && errno == EBADF);
    fíoraigh(write(Comhad, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) fíoraigh(dup(Comhad) == INDEX);
    fíoraigh(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    fíoraigh(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    fíoraigh(fstat(Comhad, &staid_VALUE) == 0 && staid_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) fíoraigh(close(INDEX) == 0);
    fíoraigh(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Comhad = open("posix.txt", O_RDONLY);
    fíoraigh(Comhad == 3 && write(Comhad, sonraí, 1) == -1 && errno == EBADF);
    fíoraigh(fcntl(Comhad, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    fíoraigh(close(8) == 0 && close(Comhad) == 0 && unlink("posix.txt") == 0);
    fíoraigh(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    fíoraigh(fstat(1, &staid_VALUE) == 0 && S_ISCHR(staid_VALUE.st_mode));
    fíoraigh(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    fíoraigh(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    fíoraigh(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    fíoraigh(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    fíoraigh(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    fíoraigh(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    fíoraigh(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    fíoraigh(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], mír_COUNT = 0; char Ainm[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Ainm[4] = '0' + INDEX;
        int 열린파일 = open(Ainm, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { fíoraigh(errno == ENOSPC); break; }
        보관[mír_COUNT++] = 열린파일;
    }
    fíoraigh(mír_COUNT > 0 && mír_COUNT < 8);
    fíoraigh(unlink("slot0") == 0);
    fíoraigh(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    fíoraigh(close(보관[0]) == 0);
    Comhad = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    fíoraigh(Comhad >= 0 && close(Comhad) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < mír_COUNT; INDEX++) {
        Ainm[4] = '0' + INDEX;
        fíoraigh(close(보관[INDEX]) == 0 && unlink(Ainm) == 0);
    }
    fíoraigh(fsync(-1) == -1 && errno == EBADF);
    fíoraigh(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
