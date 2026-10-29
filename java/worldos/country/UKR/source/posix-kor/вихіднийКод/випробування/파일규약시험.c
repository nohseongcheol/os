#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int умова, int рядок_введення) {
    검사항목수++;
    if (!умова) {
        puts("POSIX CHECK FAILED");
        char цифра_значення[12]; int 길이 = 0;
        do { цифра_значення[길이++] = '0' + рядок_введення % 10; рядок_введення /= 10; } while (рядок_введення);
        while (길이) putchar(цифра_значення[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define перевіряти(умова) 검사((умова), __LINE__)

int main(int 인수개수, char **аргумент_список) {
    char дані[32]; struct stat Стан_значення;
    перевіряти(인수개수 == 2 && strcmp(аргумент_список[1], "check") == 0 && аргумент_список[2] == 0);
    перевіряти(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    перевіряти(відкрито_Файл("absent", лише_для_читання_значення) == -1 && номер_помилки == ENOENT);
    int файл = відкрито_Файл("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    перевіряти(файл == 3);
    перевіряти(записування_Файл_дані(файл, "abcd", 4) == 4);
    перевіряти(відкрито_Файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    перевіряти(파일상태읽기(файл, &Стан_значення) == 0 && Стан_значення.st_size == 4 && S_ISREG(Стан_значення.st_mode));
    перевіряти((Стан_значення.st_mode & 0777) == 0640 && Стан_значення.st_nlink == 1);
    перевіряти(шукати_Файл(файл, 0, 처음기준) == 0);
    int клонувати_значення = 파일서술자복제(файл);
    перевіряти(клонувати_значення == 4);
    перевіряти(파일자료읽기(клонувати_значення, дані, 2) == 2 && memcmp(дані, "ab", 2) == 0);
    перевіряти(파일자료읽기(файл, дані, 2) == 2 && memcmp(дані, "cd", 2) == 0);
    перевіряти(파일자료읽기(файл, дані, 1) == 0);
    перевіряти(fcntl(файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(файл, F_GETFD) == 1);
    перевіряти(fcntl(клонувати_значення, F_GETFD) == 0);
    перевіряти(dup2(файл, файл) == файл && fcntl(файл, F_GETFD) == 1);
    перевіряти(dup2(-1, клонувати_значення) == -1 && errno == EBADF && fcntl(клонувати_значення, F_GETFD) == 0);
    перевіряти(fcntl(клонувати_значення, F_SETFL, O_APPEND) == 0 && (fcntl(файл, F_GETFL) & O_APPEND));
    перевіряти(lseek(файл, 0, SEEK_SET) == 0 && write(клонувати_значення, "e", 1) == 1 && lseek(файл, 0, SEEK_CUR) == 5);
    перевіряти(fcntl(файл, F_SETFL, 0) == 0);
    перевіряти(lseek(файл, 8, SEEK_SET) == 8 && write(файл, "Z", 1) == 1);
    перевіряти(lseek(клонувати_значення, 5, SEEK_SET) == 5 && read(файл, дані, 4) == 4);
    перевіряти(дані[0] == 0 && дані[1] == 0 && дані[2] == 0 && дані[3] == 'Z');
    перевіряти(ftruncate(файл, 2) == 0 && lseek(файл, 0, SEEK_CUR) == 9);
    перевіряти(ftruncate(файл, 6) == 0 && lseek(файл, 2, SEEK_SET) == 2 && read(файл, дані, 4) == 4);
    перевіряти(!дані[0] && !дані[1] && !дані[2] && !дані[3]);
    перевіряти(lseek(файл, 2147483647, SEEK_SET) == 2147483647);
    перевіряти(lseek(файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    перевіряти(lseek(файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    перевіряти(write(файл, "!", 1) == -1 && errno == EFBIG);
    перевіряти(lseek(файл, 0, SEEK_SET) == 0);
    перевіряти(read(файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    перевіряти(read(файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    перевіряти(write(файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    перевіряти(read(файл, дані, (size_t)-1) == -1 && errno == EINVAL);
    перевіряти(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    перевіряти(fstat(файл, (void *)0x00100000) == -1 && errno == EFAULT);
    перевіряти(lseek(файл, 0, SEEK_CUR) == 0);
    перевіряти(read(файл, NULL, 0) == 0 && write(файл, NULL, 0) == 0);
    перевіряти(вилучати_Файл_запис_ім_я("posix.txt") == 0);
    перевіряти(fstat(файл, &Стан_значення) == 0 && Стан_значення.st_nlink == 0 && Стан_значення.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    перевіряти(새파일 == 5 && fstat(새파일, &Стан_значення) == 0 && Стан_значення.st_size == 0);
    перевіряти(read(файл, дані, 2) == 2 && memcmp(дані, "ab", 2) == 0);
    перевіряти(close(файл) == 0 && close(клонувати_значення) == 0 && close(새파일) == 0);
    перевіряти(close(새파일) == -1 && errno == EBADF);
    перевіряти(unlink("posix.txt") == 0);
    файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    перевіряти(файл == 3 && fcntl(файл, F_GETFD) == 1);
    перевіряти(read(файл, дані, 1) == -1 && errno == EBADF);
    перевіряти(write(файл, "keep", 4) == 4);
    for (int індекс = 4; індекс < 32; індекс++) перевіряти(dup(файл) == індекс);
    перевіряти(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    перевіряти(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    перевіряти(fstat(файл, &Стан_значення) == 0 && Стан_значення.st_size == 4);
    for (int індекс = 3; індекс < 32; індекс++) перевіряти(close(індекс) == 0);
    перевіряти(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    файл = open("posix.txt", O_RDONLY);
    перевіряти(файл == 3 && write(файл, дані, 1) == -1 && errno == EBADF);
    перевіряти(fcntl(файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    перевіряти(close(8) == 0 && close(файл) == 0 && unlink("posix.txt") == 0);
    перевіряти(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    перевіряти(fstat(1, &Стан_значення) == 0 && S_ISCHR(Стан_значення.st_mode));
    перевіряти(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    перевіряти(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Адреса; char адреса_Текст[16];
    перевіряти(inet_pton(AF_INET, "10.0.2.2", &Адреса) == 1 && ntohl(Адреса.s_addr) == 0x0a000202U);
    перевіряти(inet_ntop(AF_INET, &Адреса, адреса_Текст, sizeof адреса_Текст) == адреса_Текст && strcmp(адреса_Текст, "10.0.2.2") == 0);
    перевіряти(inet_pton(AF_INET, "256.0.0.1", &Адреса) == 0 && ntohl(Адреса.s_addr) == 0x0a000202U);
    перевіряти(inet_pton(AF_INET, "01.0.0.1", &Адреса) == 0);
    перевіряти(inet_ntop(AF_INET, &Адреса, адреса_Текст, 3) == NULL && errno == ENOSPC);
    перевіряти(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Назва[] = "slot0";
    for (int індекс = 0; індекс < 8; індекс++) {
        Назва[4] = '0' + індекс;
        int 열린파일 = open(Назва, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { перевіряти(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    перевіряти(개수 > 0 && 개수 < 8);
    перевіряти(unlink("slot0") == 0);
    перевіряти(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    перевіряти(close(보관[0]) == 0);
    файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    перевіряти(файл >= 0 && close(файл) == 0 && unlink("held-slot") == 0);
    for (int індекс = 1; індекс < 개수; індекс++) {
        Назва[4] = '0' + індекс;
        перевіряти(close(보관[індекс]) == 0 && unlink(Назва) == 0);
    }
    перевіряти(fsync(-1) == -1 && errno == EBADF);
    перевіряти(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
