#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int шарт, int юл) {
    검사항목수++;
    if (!шарт) {
        puts("POSIX CHECK FAILED");
        char сан_VALUE[12]; int озынлык_VALUE = 0;
        do { сан_VALUE[озынлык_VALUE++] = '0' + юл % 10; юл /= 10; } while (юл);
        while (озынлык_VALUE) putchar(сан_VALUE[--озынлык_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define раслау(шарт) 검사((шарт), __LINE__)

int main(int 인수개수, char **аргумент_Исемлек) {
    char мәгълүмат[32]; struct stat халәт_VALUE;
    раслау(인수개수 == 2 && strcmp(аргумент_Исемлек[1], "check") == 0 && аргумент_Исемлек[2] == 0);
    раслау(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    раслау(ачу_файл("absent", укымалы_гына_VALUE) == -1 && 오류번호 == ENOENT);
    int Birem = ачу_файл("/posix.txt", укымалы_язмалы | 새파일만들기, 0640);
    раслау(Birem == 3);
    раслау(язу_файл_мәгълүмат(Birem, "abcd", 4) == 4);
    раслау(ачу_файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    раслау(파일상태읽기(Birem, &халәт_VALUE) == 0 && халәт_VALUE.st_size == 4 && S_ISREG(халәт_VALUE.st_mode));
    раслау((халәт_VALUE.st_mode & 0777) == 0640 && халәт_VALUE.st_nlink == 1);
    раслау(эзләү_файл(Birem, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Birem);
    раслау(복제 == 4);
    раслау(파일자료읽기(복제, мәгълүмат, 2) == 2 && memcmp(мәгълүмат, "ab", 2) == 0);
    раслау(파일자료읽기(Birem, мәгълүмат, 2) == 2 && memcmp(мәгълүмат, "cd", 2) == 0);
    раслау(파일자료읽기(Birem, мәгълүмат, 1) == 0);
    раслау(fcntl(Birem, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Birem, F_GETFD) == 1);
    раслау(fcntl(복제, F_GETFD) == 0);
    раслау(dup2(Birem, Birem) == Birem && fcntl(Birem, F_GETFD) == 1);
    раслау(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    раслау(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Birem, F_GETFL) & O_APPEND));
    раслау(lseek(Birem, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Birem, 0, SEEK_CUR) == 5);
    раслау(fcntl(Birem, F_SETFL, 0) == 0);
    раслау(lseek(Birem, 8, SEEK_SET) == 8 && write(Birem, "Z", 1) == 1);
    раслау(lseek(복제, 5, SEEK_SET) == 5 && read(Birem, мәгълүмат, 4) == 4);
    раслау(мәгълүмат[0] == 0 && мәгълүмат[1] == 0 && мәгълүмат[2] == 0 && мәгълүмат[3] == 'Z');
    раслау(ftruncate(Birem, 2) == 0 && lseek(Birem, 0, SEEK_CUR) == 9);
    раслау(ftruncate(Birem, 6) == 0 && lseek(Birem, 2, SEEK_SET) == 2 && read(Birem, мәгълүмат, 4) == 4);
    раслау(!мәгълүмат[0] && !мәгълүмат[1] && !мәгълүмат[2] && !мәгълүмат[3]);
    раслау(lseek(Birem, 2147483647, SEEK_SET) == 2147483647);
    раслау(lseek(Birem, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    раслау(lseek(Birem, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    раслау(write(Birem, "!", 1) == -1 && errno == EFBIG);
    раслау(lseek(Birem, 0, SEEK_SET) == 0);
    раслау(read(Birem, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    раслау(read(Birem, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    раслау(write(Birem, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    раслау(read(Birem, мәгълүмат, (size_t)-1) == -1 && errno == EINVAL);
    раслау(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    раслау(fstat(Birem, (void *)0x00100000) == -1 && errno == EFAULT);
    раслау(lseek(Birem, 0, SEEK_CUR) == 0);
    раслау(read(Birem, NULL, 0) == 0 && write(Birem, NULL, 0) == 0);
    раслау(бетерү_файл_кертү_исем("posix.txt") == 0);
    раслау(fstat(Birem, &халәт_VALUE) == 0 && халәт_VALUE.st_nlink == 0 && халәт_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    раслау(새파일 == 5 && fstat(새파일, &халәт_VALUE) == 0 && халәт_VALUE.st_size == 0);
    раслау(read(Birem, мәгълүмат, 2) == 2 && memcmp(мәгълүмат, "ab", 2) == 0);
    раслау(close(Birem) == 0 && close(복제) == 0 && close(새파일) == 0);
    раслау(close(새파일) == -1 && errno == EBADF);
    раслау(unlink("posix.txt") == 0);
    Birem = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    раслау(Birem == 3 && fcntl(Birem, F_GETFD) == 1);
    раслау(read(Birem, мәгълүмат, 1) == -1 && errno == EBADF);
    раслау(write(Birem, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) раслау(dup(Birem) == INDEX);
    раслау(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    раслау(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    раслау(fstat(Birem, &халәт_VALUE) == 0 && халәт_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) раслау(close(INDEX) == 0);
    раслау(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Birem = open("posix.txt", O_RDONLY);
    раслау(Birem == 3 && write(Birem, мәгълүмат, 1) == -1 && errno == EBADF);
    раслау(fcntl(Birem, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    раслау(close(8) == 0 && close(Birem) == 0 && unlink("posix.txt") == 0);
    раслау(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    раслау(fstat(1, &халәт_VALUE) == 0 && S_ISCHR(халәт_VALUE.st_mode));
    раслау(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    раслау(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr адрес; char адрес_СМС[16];
    раслау(inet_pton(AF_INET, "10.0.2.2", &адрес) == 1 && ntohl(адрес.s_addr) == 0x0a000202U);
    раслау(inet_ntop(AF_INET, &адрес, адрес_СМС, sizeof адрес_СМС) == адрес_СМС && strcmp(адрес_СМС, "10.0.2.2") == 0);
    раслау(inet_pton(AF_INET, "256.0.0.1", &адрес) == 0 && ntohl(адрес.s_addr) == 0x0a000202U);
    раслау(inet_pton(AF_INET, "01.0.0.1", &адрес) == 0);
    раслау(inet_ntop(AF_INET, &адрес, адрес_СМС, 3) == NULL && errno == ENOSPC);
    раслау(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], элемент_COUNT = 0; char исем[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        исем[4] = '0' + INDEX;
        int 열린파일 = open(исем, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { раслау(errno == ENOSPC); break; }
        보관[элемент_COUNT++] = 열린파일;
    }
    раслау(элемент_COUNT > 0 && элемент_COUNT < 8);
    раслау(unlink("slot0") == 0);
    раслау(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    раслау(close(보관[0]) == 0);
    Birem = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    раслау(Birem >= 0 && close(Birem) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < элемент_COUNT; INDEX++) {
        исем[4] = '0' + INDEX;
        раслау(close(보관[INDEX]) == 0 && unlink(исем) == 0);
    }
    раслау(fsync(-1) == -1 && errno == EBADF);
    раслау(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
