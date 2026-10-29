#include <файл_ABI.h>
#include <сеть_ABI.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int условие, int строка_ввода) {
    검사항목수++;
    if (!условие) {
        puts("POSIX CHECK FAILED");
        char цифра_ЗНАЧЕН[12]; int длина_ЗНАЧЕН = 0;
        do { цифра_ЗНАЧЕН[длина_ЗНАЧЕН++] = '0' + строка_ввода % 10; строка_ввода /= 10; } while (строка_ввода);
        while (длина_ЗНАЧЕН) putchar(цифра_ЗНАЧЕН[--длина_ЗНАЧЕН]);
        putchar('\n'); _exit(1);
    }
}
#define проверять(условие) 검사((условие), __LINE__)

int main(int 인수개수, char **аргумент_Список) {
    char данные[32]; struct stat Состояние_ЗНАЧЕН;
    проверять(인수개수 == 2 && strcmp(аргумент_Список[1], "check") == 0 && аргумент_Список[2] == 0);
    проверять(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    проверять(открыть_файл("absent", нередактируемый_ЗНАЧЕН) == -1 && номер_ошибки == ENOENT);
    int файл = открыть_файл("/posix.txt", для_чтения_и_записи | 새파일만들기, 0640);
    проверять(файл == 3);
    проверять(запись_файл_данные(файл, "abcd", 4) == 4);
    проверять(открыть_файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    проверять(чтение_файл_статус(файл, &Состояние_ЗНАЧЕН) == 0 && Состояние_ЗНАЧЕН.st_size == 4 && S_ISREG(Состояние_ЗНАЧЕН.st_mode));
    проверять((Состояние_ЗНАЧЕН.st_mode & 0777) == 0640 && Состояние_ЗНАЧЕН.st_nlink == 1);
    проверять(поиск_файл(файл, 0, 처음기준) == 0);
    int клон_ЗНАЧЕН = дубликат_файл_дескриптор(файл);
    проверять(клон_ЗНАЧЕН == 4);
    проверять(чтение_файл_данные(клон_ЗНАЧЕН, данные, 2) == 2 && memcmp(данные, "ab", 2) == 0);
    проверять(чтение_файл_данные(файл, данные, 2) == 2 && memcmp(данные, "cd", 2) == 0);
    проверять(чтение_файл_данные(файл, данные, 1) == 0);
    проверять(fcntl(файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(файл, F_GETFD) == 1);
    проверять(fcntl(клон_ЗНАЧЕН, F_GETFD) == 0);
    проверять(dup2(файл, файл) == файл && fcntl(файл, F_GETFD) == 1);
    проверять(dup2(-1, клон_ЗНАЧЕН) == -1 && errno == EBADF && fcntl(клон_ЗНАЧЕН, F_GETFD) == 0);
    проверять(fcntl(клон_ЗНАЧЕН, F_SETFL, O_APPEND) == 0 && (fcntl(файл, F_GETFL) & O_APPEND));
    проверять(lseek(файл, 0, SEEK_SET) == 0 && write(клон_ЗНАЧЕН, "e", 1) == 1 && lseek(файл, 0, SEEK_CUR) == 5);
    проверять(fcntl(файл, F_SETFL, 0) == 0);
    проверять(lseek(файл, 8, SEEK_SET) == 8 && write(файл, "Z", 1) == 1);
    проверять(lseek(клон_ЗНАЧЕН, 5, SEEK_SET) == 5 && read(файл, данные, 4) == 4);
    проверять(данные[0] == 0 && данные[1] == 0 && данные[2] == 0 && данные[3] == 'Z');
    проверять(ftruncate(файл, 2) == 0 && lseek(файл, 0, SEEK_CUR) == 9);
    проверять(ftruncate(файл, 6) == 0 && lseek(файл, 2, SEEK_SET) == 2 && read(файл, данные, 4) == 4);
    проверять(!данные[0] && !данные[1] && !данные[2] && !данные[3]);
    проверять(lseek(файл, 2147483647, SEEK_SET) == 2147483647);
    проверять(lseek(файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    проверять(lseek(файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    проверять(write(файл, "!", 1) == -1 && errno == EFBIG);
    проверять(lseek(файл, 0, SEEK_SET) == 0);
    проверять(read(файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    проверять(read(файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    проверять(write(файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    проверять(read(файл, данные, (size_t)-1) == -1 && errno == EINVAL);
    проверять(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    проверять(fstat(файл, (void *)0x00100000) == -1 && errno == EFAULT);
    проверять(lseek(файл, 0, SEEK_CUR) == 0);
    проверять(read(файл, NULL, 0) == 0 && write(файл, NULL, 0) == 0);
    проверять(удалить_файл_ввод_имя("posix.txt") == 0);
    проверять(fstat(файл, &Состояние_ЗНАЧЕН) == 0 && Состояние_ЗНАЧЕН.st_nlink == 0 && Состояние_ЗНАЧЕН.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    проверять(새파일 == 5 && fstat(새파일, &Состояние_ЗНАЧЕН) == 0 && Состояние_ЗНАЧЕН.st_size == 0);
    проверять(read(файл, данные, 2) == 2 && memcmp(данные, "ab", 2) == 0);
    проверять(close(файл) == 0 && close(клон_ЗНАЧЕН) == 0 && close(새파일) == 0);
    проверять(close(새파일) == -1 && errno == EBADF);
    проверять(unlink("posix.txt") == 0);
    файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    проверять(файл == 3 && fcntl(файл, F_GETFD) == 1);
    проверять(read(файл, данные, 1) == -1 && errno == EBADF);
    проверять(write(файл, "keep", 4) == 4);
    for (int ИНДЕКС = 4; ИНДЕКС < 32; ИНДЕКС++) проверять(dup(файл) == ИНДЕКС);
    проверять(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    проверять(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    проверять(fstat(файл, &Состояние_ЗНАЧЕН) == 0 && Состояние_ЗНАЧЕН.st_size == 4);
    for (int ИНДЕКС = 3; ИНДЕКС < 32; ИНДЕКС++) проверять(close(ИНДЕКС) == 0);
    проверять(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    файл = open("posix.txt", O_RDONLY);
    проверять(файл == 3 && write(файл, данные, 1) == -1 && errno == EBADF);
    проверять(fcntl(файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    проверять(close(8) == 0 && close(файл) == 0 && unlink("posix.txt") == 0);
    проверять(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    проверять(fstat(1, &Состояние_ЗНАЧЕН) == 0 && S_ISCHR(Состояние_ЗНАЧЕН.st_mode));
    проверять(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    проверять(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr АДРЕС; char АДРЕС_SMS[16];
    проверять(inet_pton(AF_INET, "10.0.2.2", &АДРЕС) == 1 && ntohl(АДРЕС.s_addr) == 0x0a000202U);
    проверять(inet_ntop(AF_INET, &АДРЕС, АДРЕС_SMS, sizeof АДРЕС_SMS) == АДРЕС_SMS && strcmp(АДРЕС_SMS, "10.0.2.2") == 0);
    проверять(inet_pton(AF_INET, "256.0.0.1", &АДРЕС) == 0 && ntohl(АДРЕС.s_addr) == 0x0a000202U);
    проверять(inet_pton(AF_INET, "01.0.0.1", &АДРЕС) == 0);
    проверять(inet_ntop(AF_INET, &АДРЕС, АДРЕС_SMS, 3) == NULL && errno == ENOSPC);
    проверять(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], товар_СЧЁТ = 0; char Название[] = "slot0";
    for (int ИНДЕКС = 0; ИНДЕКС < 8; ИНДЕКС++) {
        Название[4] = '0' + ИНДЕКС;
        int 열린파일 = open(Название, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { проверять(errno == ENOSPC); break; }
        보관[товар_СЧЁТ++] = 열린파일;
    }
    проверять(товар_СЧЁТ > 0 && товар_СЧЁТ < 8);
    проверять(unlink("slot0") == 0);
    проверять(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    проверять(close(보관[0]) == 0);
    файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    проверять(файл >= 0 && close(файл) == 0 && unlink("held-slot") == 0);
    for (int ИНДЕКС = 1; ИНДЕКС < товар_СЧЁТ; ИНДЕКС++) {
        Название[4] = '0' + ИНДЕКС;
        проверять(close(보관[ИНДЕКС]) == 0 && unlink(Название) == 0);
    }
    проверять(fsync(-1) == -1 && errno == EBADF);
    проверять(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
