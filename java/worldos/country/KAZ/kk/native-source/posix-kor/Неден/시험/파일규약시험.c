#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int шарт, int Жол) {
    검사항목수++;
    if (!шарт) {
        puts("POSIX CHECK FAILED");
        char сан_мән[12]; int ұзындық_мән = 0;
        do { сан_мән[ұзындық_мән++] = '0' + Жол % 10; Жол /= 10; } while (Жол);
        while (ұзындық_мән) putchar(сан_мән[--ұзындық_мән]);
        putchar('\n'); _exit(1);
    }
}
#define тексеру(шарт) 검사((шарт), __LINE__)

int main(int 인수개수, char **аргумент_Тізім) {
    char деректер[32]; struct stat күй_мән;
    тексеру(인수개수 == 2 && strcmp(аргумент_Тізім[1], "check") == 0 && аргумент_Тізім[2] == 0);
    тексеру(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    тексеру(ашу_файл("absent", тек_оқу_үшін_мән) == -1 && қате_нөмірі == ENOENT);
    int Файл = ашу_файл("/posix.txt", оқу_жазу | 새파일만들기, 0640);
    тексеру(Файл == 3);
    тексеру(жазу_файл_деректер(Файл, "abcd", 4) == 4);
    тексеру(ашу_файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    тексеру(파일상태읽기(Файл, &күй_мән) == 0 && күй_мән.st_size == 4 && S_ISREG(күй_мән.st_mode));
    тексеру((күй_мән.st_mode & 0777) == 0640 && күй_мән.st_nlink == 1);
    тексеру(іздеу_файл(Файл, 0, 처음기준) == 0);
    int клон_мән = 파일서술자복제(Файл);
    тексеру(клон_мән == 4);
    тексеру(파일자료읽기(клон_мән, деректер, 2) == 2 && memcmp(деректер, "ab", 2) == 0);
    тексеру(파일자료읽기(Файл, деректер, 2) == 2 && memcmp(деректер, "cd", 2) == 0);
    тексеру(파일자료읽기(Файл, деректер, 1) == 0);
    тексеру(fcntl(Файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Файл, F_GETFD) == 1);
    тексеру(fcntl(клон_мән, F_GETFD) == 0);
    тексеру(dup2(Файл, Файл) == Файл && fcntl(Файл, F_GETFD) == 1);
    тексеру(dup2(-1, клон_мән) == -1 && errno == EBADF && fcntl(клон_мән, F_GETFD) == 0);
    тексеру(fcntl(клон_мән, F_SETFL, O_APPEND) == 0 && (fcntl(Файл, F_GETFL) & O_APPEND));
    тексеру(lseek(Файл, 0, SEEK_SET) == 0 && write(клон_мән, "e", 1) == 1 && lseek(Файл, 0, SEEK_CUR) == 5);
    тексеру(fcntl(Файл, F_SETFL, 0) == 0);
    тексеру(lseek(Файл, 8, SEEK_SET) == 8 && write(Файл, "Z", 1) == 1);
    тексеру(lseek(клон_мән, 5, SEEK_SET) == 5 && read(Файл, деректер, 4) == 4);
    тексеру(деректер[0] == 0 && деректер[1] == 0 && деректер[2] == 0 && деректер[3] == 'Z');
    тексеру(ftruncate(Файл, 2) == 0 && lseek(Файл, 0, SEEK_CUR) == 9);
    тексеру(ftruncate(Файл, 6) == 0 && lseek(Файл, 2, SEEK_SET) == 2 && read(Файл, деректер, 4) == 4);
    тексеру(!деректер[0] && !деректер[1] && !деректер[2] && !деректер[3]);
    тексеру(lseek(Файл, 2147483647, SEEK_SET) == 2147483647);
    тексеру(lseek(Файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    тексеру(lseek(Файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    тексеру(write(Файл, "!", 1) == -1 && errno == EFBIG);
    тексеру(lseek(Файл, 0, SEEK_SET) == 0);
    тексеру(read(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    тексеру(read(Файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    тексеру(write(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    тексеру(read(Файл, деректер, (size_t)-1) == -1 && errno == EINVAL);
    тексеру(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    тексеру(fstat(Файл, (void *)0x00100000) == -1 && errno == EFAULT);
    тексеру(lseek(Файл, 0, SEEK_CUR) == 0);
    тексеру(read(Файл, NULL, 0) == 0 && write(Файл, NULL, 0) == 0);
    тексеру(жою_файл_енгізу_аты("posix.txt") == 0);
    тексеру(fstat(Файл, &күй_мән) == 0 && күй_мән.st_nlink == 0 && күй_мән.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    тексеру(새파일 == 5 && fstat(새파일, &күй_мән) == 0 && күй_мән.st_size == 0);
    тексеру(read(Файл, деректер, 2) == 2 && memcmp(деректер, "ab", 2) == 0);
    тексеру(close(Файл) == 0 && close(клон_мән) == 0 && close(새파일) == 0);
    тексеру(close(새파일) == -1 && errno == EBADF);
    тексеру(unlink("posix.txt") == 0);
    Файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    тексеру(Файл == 3 && fcntl(Файл, F_GETFD) == 1);
    тексеру(read(Файл, деректер, 1) == -1 && errno == EBADF);
    тексеру(write(Файл, "keep", 4) == 4);
    for (int индекс = 4; индекс < 32; индекс++) тексеру(dup(Файл) == индекс);
    тексеру(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    тексеру(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    тексеру(fstat(Файл, &күй_мән) == 0 && күй_мән.st_size == 4);
    for (int индекс = 3; индекс < 32; индекс++) тексеру(close(индекс) == 0);
    тексеру(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Файл = open("posix.txt", O_RDONLY);
    тексеру(Файл == 3 && write(Файл, деректер, 1) == -1 && errno == EBADF);
    тексеру(fcntl(Файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    тексеру(close(8) == 0 && close(Файл) == 0 && unlink("posix.txt") == 0);
    тексеру(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    тексеру(fstat(1, &күй_мән) == 0 && S_ISCHR(күй_мән.st_mode));
    тексеру(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    тексеру(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr мекенжай; char мекенжай_Мәтін[16];
    тексеру(inet_pton(AF_INET, "10.0.2.2", &мекенжай) == 1 && ntohl(мекенжай.s_addr) == 0x0a000202U);
    тексеру(inet_ntop(AF_INET, &мекенжай, мекенжай_Мәтін, sizeof мекенжай_Мәтін) == мекенжай_Мәтін && strcmp(мекенжай_Мәтін, "10.0.2.2") == 0);
    тексеру(inet_pton(AF_INET, "256.0.0.1", &мекенжай) == 0 && ntohl(мекенжай.s_addr) == 0x0a000202U);
    тексеру(inet_pton(AF_INET, "01.0.0.1", &мекенжай) == 0);
    тексеру(inet_ntop(AF_INET, &мекенжай, мекенжай_Мәтін, 3) == NULL && errno == ENOSPC);
    тексеру(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Аты[] = "slot0";
    for (int индекс = 0; индекс < 8; индекс++) {
        Аты[4] = '0' + индекс;
        int 열린파일 = open(Аты, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { тексеру(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    тексеру(개수 > 0 && 개수 < 8);
    тексеру(unlink("slot0") == 0);
    тексеру(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    тексеру(close(보관[0]) == 0);
    Файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    тексеру(Файл >= 0 && close(Файл) == 0 && unlink("held-slot") == 0);
    for (int индекс = 1; индекс < 개수; индекс++) {
        Аты[4] = '0' + индекс;
        тексеру(close(보관[индекс]) == 0 && unlink(Аты) == 0);
    }
    тексеру(fsync(-1) == -1 && errno == EBADF);
    тексеру(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
