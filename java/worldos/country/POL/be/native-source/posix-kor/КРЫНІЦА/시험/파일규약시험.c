#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int умова, int лінія) {
    검사항목수++;
    if (!умова) {
        puts("POSIX CHECK FAILED");
        char лічба_значэнне[12]; int даўжыня_значэнне = 0;
        do { лічба_значэнне[даўжыня_значэнне++] = '0' + лінія % 10; лінія /= 10; } while (лінія);
        while (даўжыня_значэнне) putchar(лічба_значэнне[--даўжыня_значэнне]);
        putchar('\n'); _exit(1);
    }
}
#define праверыць(умова) 검사((умова), __LINE__)

int main(int 인수개수, char **аргумент_Спіс) {
    char дадзеныя[32]; struct stat стан_значэнне;
    праверыць(인수개수 == 2 && strcmp(аргумент_Спіс[1], "check") == 0 && аргумент_Спіс[2] == 0);
    праверыць(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    праверыць(адкрыць_файл("absent", толькі_для_чытання_значэнне) == -1 && 오류번호 == ENOENT);
    int Файл = адкрыць_файл("/posix.txt", для_чытання_для_запісу | 새파일만들기, 0640);
    праверыць(Файл == 3);
    праверыць(напісаць_файл_дадзеныя(Файл, "abcd", 4) == 4);
    праверыць(адкрыць_файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    праверыць(파일상태읽기(Файл, &стан_значэнне) == 0 && стан_значэнне.st_size == 4 && S_ISREG(стан_значэнне.st_mode));
    праверыць((стан_значэнне.st_mode & 0777) == 0640 && стан_значэнне.st_nlink == 1);
    праверыць(шукаць_файл(Файл, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Файл);
    праверыць(복제 == 4);
    праверыць(파일자료읽기(복제, дадзеныя, 2) == 2 && memcmp(дадзеныя, "ab", 2) == 0);
    праверыць(파일자료읽기(Файл, дадзеныя, 2) == 2 && memcmp(дадзеныя, "cd", 2) == 0);
    праверыць(파일자료읽기(Файл, дадзеныя, 1) == 0);
    праверыць(fcntl(Файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Файл, F_GETFD) == 1);
    праверыць(fcntl(복제, F_GETFD) == 0);
    праверыць(dup2(Файл, Файл) == Файл && fcntl(Файл, F_GETFD) == 1);
    праверыць(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    праверыць(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Файл, F_GETFL) & O_APPEND));
    праверыць(lseek(Файл, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Файл, 0, SEEK_CUR) == 5);
    праверыць(fcntl(Файл, F_SETFL, 0) == 0);
    праверыць(lseek(Файл, 8, SEEK_SET) == 8 && write(Файл, "Z", 1) == 1);
    праверыць(lseek(복제, 5, SEEK_SET) == 5 && read(Файл, дадзеныя, 4) == 4);
    праверыць(дадзеныя[0] == 0 && дадзеныя[1] == 0 && дадзеныя[2] == 0 && дадзеныя[3] == 'Z');
    праверыць(ftruncate(Файл, 2) == 0 && lseek(Файл, 0, SEEK_CUR) == 9);
    праверыць(ftruncate(Файл, 6) == 0 && lseek(Файл, 2, SEEK_SET) == 2 && read(Файл, дадзеныя, 4) == 4);
    праверыць(!дадзеныя[0] && !дадзеныя[1] && !дадзеныя[2] && !дадзеныя[3]);
    праверыць(lseek(Файл, 2147483647, SEEK_SET) == 2147483647);
    праверыць(lseek(Файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    праверыць(lseek(Файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    праверыць(write(Файл, "!", 1) == -1 && errno == EFBIG);
    праверыць(lseek(Файл, 0, SEEK_SET) == 0);
    праверыць(read(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    праверыць(read(Файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    праверыць(write(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    праверыць(read(Файл, дадзеныя, (size_t)-1) == -1 && errno == EINVAL);
    праверыць(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    праверыць(fstat(Файл, (void *)0x00100000) == -1 && errno == EFAULT);
    праверыць(lseek(Файл, 0, SEEK_CUR) == 0);
    праверыць(read(Файл, NULL, 0) == 0 && write(Файл, NULL, 0) == 0);
    праверыць(выдаліць_файл_увядзенне_імя("posix.txt") == 0);
    праверыць(fstat(Файл, &стан_значэнне) == 0 && стан_значэнне.st_nlink == 0 && стан_значэнне.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    праверыць(새파일 == 5 && fstat(새파일, &стан_значэнне) == 0 && стан_значэнне.st_size == 0);
    праверыць(read(Файл, дадзеныя, 2) == 2 && memcmp(дадзеныя, "ab", 2) == 0);
    праверыць(close(Файл) == 0 && close(복제) == 0 && close(새파일) == 0);
    праверыць(close(새파일) == -1 && errno == EBADF);
    праверыць(unlink("posix.txt") == 0);
    Файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    праверыць(Файл == 3 && fcntl(Файл, F_GETFD) == 1);
    праверыць(read(Файл, дадзеныя, 1) == -1 && errno == EBADF);
    праверыць(write(Файл, "keep", 4) == 4);
    for (int індэкс = 4; індэкс < 32; індэкс++) праверыць(dup(Файл) == індэкс);
    праверыць(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    праверыць(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    праверыць(fstat(Файл, &стан_значэнне) == 0 && стан_значэнне.st_size == 4);
    for (int індэкс = 3; індэкс < 32; індэкс++) праверыць(close(індэкс) == 0);
    праверыць(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Файл = open("posix.txt", O_RDONLY);
    праверыць(Файл == 3 && write(Файл, дадзеныя, 1) == -1 && errno == EBADF);
    праверыць(fcntl(Файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    праверыць(close(8) == 0 && close(Файл) == 0 && unlink("posix.txt") == 0);
    праверыць(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    праверыць(fstat(1, &стан_значэнне) == 0 && S_ISCHR(стан_значэнне.st_mode));
    праверыць(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    праверыць(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr адрас; char адрас_Тэкст[16];
    праверыць(inet_pton(AF_INET, "10.0.2.2", &адрас) == 1 && ntohl(адрас.s_addr) == 0x0a000202U);
    праверыць(inet_ntop(AF_INET, &адрас, адрас_Тэкст, sizeof адрас_Тэкст) == адрас_Тэкст && strcmp(адрас_Тэкст, "10.0.2.2") == 0);
    праверыць(inet_pton(AF_INET, "256.0.0.1", &адрас) == 0 && ntohl(адрас.s_addr) == 0x0a000202U);
    праверыць(inet_pton(AF_INET, "01.0.0.1", &адрас) == 0);
    праверыць(inet_ntop(AF_INET, &адрас, адрас_Тэкст, 3) == NULL && errno == ENOSPC);
    праверыць(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Назва[] = "slot0";
    for (int індэкс = 0; індэкс < 8; індэкс++) {
        Назва[4] = '0' + індэкс;
        int 열린파일 = open(Назва, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { праверыць(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    праверыць(개수 > 0 && 개수 < 8);
    праверыць(unlink("slot0") == 0);
    праверыць(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    праверыць(close(보관[0]) == 0);
    Файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    праверыць(Файл >= 0 && close(Файл) == 0 && unlink("held-slot") == 0);
    for (int індэкс = 1; індэкс < 개수; індэкс++) {
        Назва[4] = '0' + індэкс;
        праверыць(close(보관[індэкс]) == 0 && unlink(Назва) == 0);
    }
    праверыць(fsync(-1) == -1 && errno == EBADF);
    праверыць(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
