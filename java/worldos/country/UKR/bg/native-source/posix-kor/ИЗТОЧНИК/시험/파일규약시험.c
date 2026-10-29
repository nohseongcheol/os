#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int условие, int ред) {
    검사항목수++;
    if (!условие) {
        puts("POSIX CHECK FAILED");
        char цифра_стойност[12]; int 길이 = 0;
        do { цифра_стойност[길이++] = '0' + ред % 10; ред /= 10; } while (ред);
        while (길이) putchar(цифра_стойност[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define проверявам(условие) 검사((условие), __LINE__)

int main(int 인수개수, char **аргумент_Списък) {
    char данни[32]; struct stat Състояние_стойност;
    проверявам(인수개수 == 2 && strcmp(аргумент_Списък[1], "check") == 0 && аргумент_Списък[2] == 0);
    проверявам(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    проверявам(отварям_Файл("absent", само_за_четене_стойност) == -1 && Номер_на_грешка == ENOENT);
    int Файл = отварям_Файл("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    проверявам(Файл == 3);
    проверявам(записване_Файл_данни(Файл, "abcd", 4) == 4);
    проверявам(отварям_Файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    проверявам(파일상태읽기(Файл, &Състояние_стойност) == 0 && Състояние_стойност.st_size == 4 && S_ISREG(Състояние_стойност.st_mode));
    проверявам((Състояние_стойност.st_mode & 0777) == 0640 && Състояние_стойност.st_nlink == 1);
    проверявам(търся_Файл(Файл, 0, 처음기준) == 0);
    int клонирам_стойност = 파일서술자복제(Файл);
    проверявам(клонирам_стойност == 4);
    проверявам(파일자료읽기(клонирам_стойност, данни, 2) == 2 && memcmp(данни, "ab", 2) == 0);
    проверявам(파일자료읽기(Файл, данни, 2) == 2 && memcmp(данни, "cd", 2) == 0);
    проверявам(파일자료읽기(Файл, данни, 1) == 0);
    проверявам(fcntl(Файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Файл, F_GETFD) == 1);
    проверявам(fcntl(клонирам_стойност, F_GETFD) == 0);
    проверявам(dup2(Файл, Файл) == Файл && fcntl(Файл, F_GETFD) == 1);
    проверявам(dup2(-1, клонирам_стойност) == -1 && errno == EBADF && fcntl(клонирам_стойност, F_GETFD) == 0);
    проверявам(fcntl(клонирам_стойност, F_SETFL, O_APPEND) == 0 && (fcntl(Файл, F_GETFL) & O_APPEND));
    проверявам(lseek(Файл, 0, SEEK_SET) == 0 && write(клонирам_стойност, "e", 1) == 1 && lseek(Файл, 0, SEEK_CUR) == 5);
    проверявам(fcntl(Файл, F_SETFL, 0) == 0);
    проверявам(lseek(Файл, 8, SEEK_SET) == 8 && write(Файл, "Z", 1) == 1);
    проверявам(lseek(клонирам_стойност, 5, SEEK_SET) == 5 && read(Файл, данни, 4) == 4);
    проверявам(данни[0] == 0 && данни[1] == 0 && данни[2] == 0 && данни[3] == 'Z');
    проверявам(ftruncate(Файл, 2) == 0 && lseek(Файл, 0, SEEK_CUR) == 9);
    проверявам(ftruncate(Файл, 6) == 0 && lseek(Файл, 2, SEEK_SET) == 2 && read(Файл, данни, 4) == 4);
    проверявам(!данни[0] && !данни[1] && !данни[2] && !данни[3]);
    проверявам(lseek(Файл, 2147483647, SEEK_SET) == 2147483647);
    проверявам(lseek(Файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    проверявам(lseek(Файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    проверявам(write(Файл, "!", 1) == -1 && errno == EFBIG);
    проверявам(lseek(Файл, 0, SEEK_SET) == 0);
    проверявам(read(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    проверявам(read(Файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    проверявам(write(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    проверявам(read(Файл, данни, (size_t)-1) == -1 && errno == EINVAL);
    проверявам(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    проверявам(fstat(Файл, (void *)0x00100000) == -1 && errno == EFAULT);
    проверявам(lseek(Файл, 0, SEEK_CUR) == 0);
    проверявам(read(Файл, NULL, 0) == 0 && write(Файл, NULL, 0) == 0);
    проверявам(премахвам_Файл_запис_препратка_към_клетка("posix.txt") == 0);
    проверявам(fstat(Файл, &Състояние_стойност) == 0 && Състояние_стойност.st_nlink == 0 && Състояние_стойност.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    проверявам(새파일 == 5 && fstat(새파일, &Състояние_стойност) == 0 && Състояние_стойност.st_size == 0);
    проверявам(read(Файл, данни, 2) == 2 && memcmp(данни, "ab", 2) == 0);
    проверявам(close(Файл) == 0 && close(клонирам_стойност) == 0 && close(새파일) == 0);
    проверявам(close(새파일) == -1 && errno == EBADF);
    проверявам(unlink("posix.txt") == 0);
    Файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    проверявам(Файл == 3 && fcntl(Файл, F_GETFD) == 1);
    проверявам(read(Файл, данни, 1) == -1 && errno == EBADF);
    проверявам(write(Файл, "keep", 4) == 4);
    for (int индекс = 4; индекс < 32; индекс++) проверявам(dup(Файл) == индекс);
    проверявам(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    проверявам(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    проверявам(fstat(Файл, &Състояние_стойност) == 0 && Състояние_стойност.st_size == 4);
    for (int индекс = 3; индекс < 32; индекс++) проверявам(close(индекс) == 0);
    проверявам(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Файл = open("posix.txt", O_RDONLY);
    проверявам(Файл == 3 && write(Файл, данни, 1) == -1 && errno == EBADF);
    проверявам(fcntl(Файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    проверявам(close(8) == 0 && close(Файл) == 0 && unlink("posix.txt") == 0);
    проверявам(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    проверявам(fstat(1, &Състояние_стойност) == 0 && S_ISCHR(Състояние_стойност.st_mode));
    проверявам(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    проверявам(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr адрес; char адрес_Текст[16];
    проверявам(inet_pton(AF_INET, "10.0.2.2", &адрес) == 1 && ntohl(адрес.s_addr) == 0x0a000202U);
    проверявам(inet_ntop(AF_INET, &адрес, адрес_Текст, sizeof адрес_Текст) == адрес_Текст && strcmp(адрес_Текст, "10.0.2.2") == 0);
    проверявам(inet_pton(AF_INET, "256.0.0.1", &адрес) == 0 && ntohl(адрес.s_addr) == 0x0a000202U);
    проверявам(inet_pton(AF_INET, "01.0.0.1", &адрес) == 0);
    проверявам(inet_ntop(AF_INET, &адрес, адрес_Текст, 3) == NULL && errno == ENOSPC);
    проверявам(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Име[] = "slot0";
    for (int индекс = 0; индекс < 8; индекс++) {
        Име[4] = '0' + индекс;
        int 열린파일 = open(Име, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { проверявам(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    проверявам(개수 > 0 && 개수 < 8);
    проверявам(unlink("slot0") == 0);
    проверявам(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    проверявам(close(보관[0]) == 0);
    Файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    проверявам(Файл >= 0 && close(Файл) == 0 && unlink("held-slot") == 0);
    for (int индекс = 1; индекс < 개수; индекс++) {
        Име[4] = '0' + индекс;
        проверявам(close(보관[индекс]) == 0 && unlink(Име) == 0);
    }
    проверявам(fsync(-1) == -1 && errno == EBADF);
    проверявам(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
