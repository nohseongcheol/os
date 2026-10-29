#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int තත්වය, int පේළිය) {
    검사항목수++;
    if (!තත්වය) {
        puts("POSIX CHECK FAILED");
        char සංඛ්_යාංකය_අගය[12]; int දිග_අගය = 0;
        do { සංඛ්_යාංකය_අගය[දිග_අගය++] = '0' + පේළිය % 10; පේළිය /= 10; } while (පේළිය);
        while (දිග_අගය) putchar(සංඛ්_යාංකය_අගය[--දිග_අගය]);
        putchar('\n'); _exit(1);
    }
}
#define තහවුරු_කරන්න(තත්වය) 검사((තත්වය), __LINE__)

int main(int 인수개수, char **විස්තාරකය_ලැයිස්තුව) {
    char දත්ත[32]; struct stat තත්වය_අගය;
    තහවුරු_කරන්න(인수개수 == 2 && strcmp(විස්තාරකය_ලැයිස්තුව[1], "check") == 0 && විස්තාරකය_ලැයිස්තුව[2] == 0);
    තහවුරු_කරන්න(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    තහවුරු_කරන්න(සාදන්න_ගොනුව("absent", කියවීම්_පමණි_අගය) == -1 && 오류번호 == ENOENT);
    int ගොනු = සාදන්න_ගොනුව("/posix.txt", කියවීම්_ලිවීම් | 새파일만들기, 0640);
    තහවුරු_කරන්න(ගොනු == 3);
    තහවුරු_කරන්න(ලියන්න_ගොනුව_දත්ත(ගොනු, "abcd", 4) == 4);
    තහවුරු_කරන්න(සාදන්න_ගොනුව("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    තහවුරු_කරන්න(파일상태읽기(ගොනු, &තත්වය_අගය) == 0 && තත්වය_අගය.st_size == 4 && S_ISREG(තත්වය_අගය.st_mode));
    තහවුරු_කරන්න((තත්වය_අගය.st_mode & 0777) == 0640 && තත්වය_අගය.st_nlink == 1);
    තහවුරු_කරන්න(සොයන්න_ගොනුව(ගොනු, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ගොනු);
    තහවුරු_කරන්න(복제 == 4);
    තහවුරු_කරන්න(파일자료읽기(복제, දත්ත, 2) == 2 && memcmp(දත්ත, "ab", 2) == 0);
    තහවුරු_කරන්න(파일자료읽기(ගොනු, දත්ත, 2) == 2 && memcmp(දත්ත, "cd", 2) == 0);
    තහවුරු_කරන්න(파일자료읽기(ගොනු, දත්ත, 1) == 0);
    තහවුරු_කරන්න(fcntl(ගොනු, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ගොනු, F_GETFD) == 1);
    තහවුරු_කරන්න(fcntl(복제, F_GETFD) == 0);
    තහවුරු_කරන්න(dup2(ගොනු, ගොනු) == ගොනු && fcntl(ගොනු, F_GETFD) == 1);
    තහවුරු_කරන්න(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    තහවුරු_කරන්න(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ගොනු, F_GETFL) & O_APPEND));
    තහවුරු_කරන්න(lseek(ගොනු, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ගොනු, 0, SEEK_CUR) == 5);
    තහවුරු_කරන්න(fcntl(ගොනු, F_SETFL, 0) == 0);
    තහවුරු_කරන්න(lseek(ගොනු, 8, SEEK_SET) == 8 && write(ගොනු, "Z", 1) == 1);
    තහවුරු_කරන්න(lseek(복제, 5, SEEK_SET) == 5 && read(ගොනු, දත්ත, 4) == 4);
    තහවුරු_කරන්න(දත්ත[0] == 0 && දත්ත[1] == 0 && දත්ත[2] == 0 && දත්ත[3] == 'Z');
    තහවුරු_කරන්න(ftruncate(ගොනු, 2) == 0 && lseek(ගොනු, 0, SEEK_CUR) == 9);
    තහවුරු_කරන්න(ftruncate(ගොනු, 6) == 0 && lseek(ගොනු, 2, SEEK_SET) == 2 && read(ගොනු, දත්ත, 4) == 4);
    තහවුරු_කරන්න(!දත්ත[0] && !දත්ත[1] && !දත්ත[2] && !දත්ත[3]);
    තහවුරු_කරන්න(lseek(ගොනු, 2147483647, SEEK_SET) == 2147483647);
    තහවුරු_කරන්න(lseek(ගොනු, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    තහවුරු_කරන්න(lseek(ගොනු, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    තහවුරු_කරන්න(write(ගොනු, "!", 1) == -1 && errno == EFBIG);
    තහවුරු_කරන්න(lseek(ගොනු, 0, SEEK_SET) == 0);
    තහවුරු_කරන්න(read(ගොනු, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    තහවුරු_කරන්න(read(ගොනු, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    තහවුරු_කරන්න(write(ගොනු, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    තහවුරු_කරන්න(read(ගොනු, දත්ත, (size_t)-1) == -1 && errno == EINVAL);
    තහවුරු_කරන්න(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    තහවුරු_කරන්න(fstat(ගොනු, (void *)0x00100000) == -1 && errno == EFAULT);
    තහවුරු_කරන්න(lseek(ගොනු, 0, SEEK_CUR) == 0);
    තහවුරු_කරන්න(read(ගොනු, NULL, 0) == 0 && write(ගොනු, NULL, 0) == 0);
    තහවුරු_කරන්න(ඉවත්_කරන්න_ගොනුව_පිවිසුම_නම("posix.txt") == 0);
    තහවුරු_කරන්න(fstat(ගොනු, &තත්වය_අගය) == 0 && තත්වය_අගය.st_nlink == 0 && තත්වය_අගය.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    තහවුරු_කරන්න(새파일 == 5 && fstat(새파일, &තත්වය_අගය) == 0 && තත්වය_අගය.st_size == 0);
    තහවුරු_කරන්න(read(ගොනු, දත්ත, 2) == 2 && memcmp(දත්ත, "ab", 2) == 0);
    තහවුරු_කරන්න(close(ගොනු) == 0 && close(복제) == 0 && close(새파일) == 0);
    තහවුරු_කරන්න(close(새파일) == -1 && errno == EBADF);
    තහවුරු_කරන්න(unlink("posix.txt") == 0);
    ගොනු = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    තහවුරු_කරන්න(ගොනු == 3 && fcntl(ගොනු, F_GETFD) == 1);
    තහවුරු_කරන්න(read(ගොනු, දත්ත, 1) == -1 && errno == EBADF);
    තහවුරු_කරන්න(write(ගොනු, "keep", 4) == 4);
    for (int සූචිය = 4; සූචිය < 32; සූචිය++) තහවුරු_කරන්න(dup(ගොනු) == සූචිය);
    තහවුරු_කරන්න(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    තහවුරු_කරන්න(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    තහවුරු_කරන්න(fstat(ගොනු, &තත්වය_අගය) == 0 && තත්වය_අගය.st_size == 4);
    for (int සූචිය = 3; සූචිය < 32; සූචිය++) තහවුරු_කරන්න(close(සූචිය) == 0);
    තහවුරු_කරන්න(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ගොනු = open("posix.txt", O_RDONLY);
    තහවුරු_කරන්න(ගොනු == 3 && write(ගොනු, දත්ත, 1) == -1 && errno == EBADF);
    තහවුරු_කරන්න(fcntl(ගොනු, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    තහවුරු_කරන්න(close(8) == 0 && close(ගොනු) == 0 && unlink("posix.txt") == 0);
    තහවුරු_කරන්න(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    තහවුරු_කරන්න(fstat(1, &තත්වය_අගය) == 0 && S_ISCHR(තත්වය_අගය.st_mode));
    තහවුරු_කරන්න(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    තහවුරු_කරන්න(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr යොමුව; char යොමුව_පෙළ[16];
    තහවුරු_කරන්න(inet_pton(AF_INET, "10.0.2.2", &යොමුව) == 1 && ntohl(යොමුව.s_addr) == 0x0a000202U);
    තහවුරු_කරන්න(inet_ntop(AF_INET, &යොමුව, යොමුව_පෙළ, sizeof යොමුව_පෙළ) == යොමුව_පෙළ && strcmp(යොමුව_පෙළ, "10.0.2.2") == 0);
    තහවුරු_කරන්න(inet_pton(AF_INET, "256.0.0.1", &යොමුව) == 0 && ntohl(යොමුව.s_addr) == 0x0a000202U);
    තහවුරු_කරන්න(inet_pton(AF_INET, "01.0.0.1", &යොමුව) == 0);
    තහවුරු_කරන්න(inet_ntop(AF_INET, &යොමුව, යොමුව_පෙළ, 3) == NULL && errno == ENOSPC);
    තහවුරු_කරන්න(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char නම[] = "slot0";
    for (int සූචිය = 0; සූචිය < 8; සූචිය++) {
        නම[4] = '0' + සූචිය;
        int 열린파일 = open(නම, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { තහවුරු_කරන්න(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    තහවුරු_කරන්න(개수 > 0 && 개수 < 8);
    තහවුරු_කරන්න(unlink("slot0") == 0);
    තහවුරු_කරන්න(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    තහවුරු_කරන්න(close(보관[0]) == 0);
    ගොනු = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    තහවුරු_කරන්න(ගොනු >= 0 && close(ගොනු) == 0 && unlink("held-slot") == 0);
    for (int සූචිය = 1; සූචිය < 개수; සූචිය++) {
        නම[4] = '0' + සූචිය;
        තහවුරු_කරන්න(close(보관[සූචිය]) == 0 && unlink(නම) == 0);
    }
    තහවුරු_කරන්න(fsync(-1) == -1 && errno == EBADF);
    තහවුරු_කරන්න(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
