#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int шарт, int хат) {
    검사항목수++;
    if (!шарт) {
        puts("POSIX CHECK FAILED");
        char рақам_қимат[12]; int дарозӣ_қимат = 0;
        do { рақам_қимат[дарозӣ_қимат++] = '0' + хат % 10; хат /= 10; } while (хат);
        while (дарозӣ_қимат) putchar(рақам_қимат[--дарозӣ_қимат]);
        putchar('\n'); _exit(1);
    }
}
#define тасдиқ_кардан(шарт) 검사((шарт), __LINE__)

int main(int 인수개수, char **аргумент_Рӯйхат) {
    char иттилоот[32]; struct stat вазъият_қимат;
    тасдиқ_кардан(인수개수 == 2 && strcmp(аргумент_Рӯйхат[1], "check") == 0 && аргумент_Рӯйхат[2] == 0);
    тасдиқ_кардан(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    тасдиқ_кардан(кушодан_файл("absent", танҳо_барои_хондан_қимат) == -1 && 오류번호 == ENOENT);
    int Файл = кушодан_файл("/posix.txt", хондан_навиштан | 새파일만들기, 0640);
    тасдиқ_кардан(Файл == 3);
    тасдиқ_кардан(навиштан_файл_иттилоот(Файл, "abcd", 4) == 4);
    тасдиқ_кардан(кушодан_файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    тасдиқ_кардан(파일상태읽기(Файл, &вазъият_қимат) == 0 && вазъият_қимат.st_size == 4 && S_ISREG(вазъият_қимат.st_mode));
    тасдиқ_кардан((вазъият_қимат.st_mode & 0777) == 0640 && вазъият_қимат.st_nlink == 1);
    тасдиқ_кардан(ҷустан_файл(Файл, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Файл);
    тасдиқ_кардан(복제 == 4);
    тасдиқ_кардан(파일자료읽기(복제, иттилоот, 2) == 2 && memcmp(иттилоот, "ab", 2) == 0);
    тасдиқ_кардан(파일자료읽기(Файл, иттилоот, 2) == 2 && memcmp(иттилоот, "cd", 2) == 0);
    тасдиқ_кардан(파일자료읽기(Файл, иттилоот, 1) == 0);
    тасдиқ_кардан(fcntl(Файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Файл, F_GETFD) == 1);
    тасдиқ_кардан(fcntl(복제, F_GETFD) == 0);
    тасдиқ_кардан(dup2(Файл, Файл) == Файл && fcntl(Файл, F_GETFD) == 1);
    тасдиқ_кардан(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    тасдиқ_кардан(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Файл, F_GETFL) & O_APPEND));
    тасдиқ_кардан(lseek(Файл, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Файл, 0, SEEK_CUR) == 5);
    тасдиқ_кардан(fcntl(Файл, F_SETFL, 0) == 0);
    тасдиқ_кардан(lseek(Файл, 8, SEEK_SET) == 8 && write(Файл, "Z", 1) == 1);
    тасдиқ_кардан(lseek(복제, 5, SEEK_SET) == 5 && read(Файл, иттилоот, 4) == 4);
    тасдиқ_кардан(иттилоот[0] == 0 && иттилоот[1] == 0 && иттилоот[2] == 0 && иттилоот[3] == 'Z');
    тасдиқ_кардан(ftruncate(Файл, 2) == 0 && lseek(Файл, 0, SEEK_CUR) == 9);
    тасдиқ_кардан(ftruncate(Файл, 6) == 0 && lseek(Файл, 2, SEEK_SET) == 2 && read(Файл, иттилоот, 4) == 4);
    тасдиқ_кардан(!иттилоот[0] && !иттилоот[1] && !иттилоот[2] && !иттилоот[3]);
    тасдиқ_кардан(lseek(Файл, 2147483647, SEEK_SET) == 2147483647);
    тасдиқ_кардан(lseek(Файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    тасдиқ_кардан(lseek(Файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    тасдиқ_кардан(write(Файл, "!", 1) == -1 && errno == EFBIG);
    тасдиқ_кардан(lseek(Файл, 0, SEEK_SET) == 0);
    тасдиқ_кардан(read(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    тасдиқ_кардан(read(Файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    тасдиқ_кардан(write(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    тасдиқ_кардан(read(Файл, иттилоот, (size_t)-1) == -1 && errno == EINVAL);
    тасдиқ_кардан(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    тасдиқ_кардан(fstat(Файл, (void *)0x00100000) == -1 && errno == EFAULT);
    тасдиқ_кардан(lseek(Файл, 0, SEEK_CUR) == 0);
    тасдиқ_кардан(read(Файл, NULL, 0) == 0 && write(Файл, NULL, 0) == 0);
    тасдиқ_кардан(тоза_кардан_файл_ворида_ном("posix.txt") == 0);
    тасдиқ_кардан(fstat(Файл, &вазъият_қимат) == 0 && вазъият_қимат.st_nlink == 0 && вазъият_қимат.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    тасдиқ_кардан(새파일 == 5 && fstat(새파일, &вазъият_қимат) == 0 && вазъият_қимат.st_size == 0);
    тасдиқ_кардан(read(Файл, иттилоот, 2) == 2 && memcmp(иттилоот, "ab", 2) == 0);
    тасдиқ_кардан(close(Файл) == 0 && close(복제) == 0 && close(새파일) == 0);
    тасдиқ_кардан(close(새파일) == -1 && errno == EBADF);
    тасдиқ_кардан(unlink("posix.txt") == 0);
    Файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    тасдиқ_кардан(Файл == 3 && fcntl(Файл, F_GETFD) == 1);
    тасдиқ_кардан(read(Файл, иттилоот, 1) == -1 && errno == EBADF);
    тасдиқ_кардан(write(Файл, "keep", 4) == 4);
    for (int индекс = 4; индекс < 32; индекс++) тасдиқ_кардан(dup(Файл) == индекс);
    тасдиқ_кардан(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    тасдиқ_кардан(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    тасдиқ_кардан(fstat(Файл, &вазъият_қимат) == 0 && вазъият_қимат.st_size == 4);
    for (int индекс = 3; индекс < 32; индекс++) тасдиқ_кардан(close(индекс) == 0);
    тасдиқ_кардан(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Файл = open("posix.txt", O_RDONLY);
    тасдиқ_кардан(Файл == 3 && write(Файл, иттилоот, 1) == -1 && errno == EBADF);
    тасдиқ_кардан(fcntl(Файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    тасдиқ_кардан(close(8) == 0 && close(Файл) == 0 && unlink("posix.txt") == 0);
    тасдиқ_кардан(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    тасдиқ_кардан(fstat(1, &вазъият_қимат) == 0 && S_ISCHR(вазъият_қимат.st_mode));
    тасдиқ_кардан(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    тасдиқ_кардан(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr суроға; char суроға_Матн[16];
    тасдиқ_кардан(inet_pton(AF_INET, "10.0.2.2", &суроға) == 1 && ntohl(суроға.s_addr) == 0x0a000202U);
    тасдиқ_кардан(inet_ntop(AF_INET, &суроға, суроға_Матн, sizeof суроға_Матн) == суроға_Матн && strcmp(суроға_Матн, "10.0.2.2") == 0);
    тасдиқ_кардан(inet_pton(AF_INET, "256.0.0.1", &суроға) == 0 && ntohl(суроға.s_addr) == 0x0a000202U);
    тасдиқ_кардан(inet_pton(AF_INET, "01.0.0.1", &суроға) == 0);
    тасдиқ_кардан(inet_ntop(AF_INET, &суроға, суроға_Матн, 3) == NULL && errno == ENOSPC);
    тасдиқ_кардан(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Ном[] = "slot0";
    for (int индекс = 0; индекс < 8; индекс++) {
        Ном[4] = '0' + индекс;
        int 열린파일 = open(Ном, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { тасдиқ_кардан(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    тасдиқ_кардан(개수 > 0 && 개수 < 8);
    тасдиқ_кардан(unlink("slot0") == 0);
    тасдиқ_кардан(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    тасдиқ_кардан(close(보관[0]) == 0);
    Файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    тасдиқ_кардан(Файл >= 0 && close(Файл) == 0 && unlink("held-slot") == 0);
    for (int индекс = 1; индекс < 개수; индекс++) {
        Ном[4] = '0' + индекс;
        тасдиқ_кардан(close(보관[индекс]) == 0 && unlink(Ном) == 0);
    }
    тасдиқ_кардан(fsync(-1) == -1 && errno == EBADF);
    тасдиқ_кардан(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
