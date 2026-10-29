#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int нөхцөл, int Шугам) {
    검사항목수++;
    if (!нөхцөл) {
        puts("POSIX CHECK FAILED");
        char тоо_утга[12]; int урт_утга = 0;
        do { тоо_утга[урт_утга++] = '0' + Шугам % 10; Шугам /= 10; } while (Шугам);
        while (урт_утга) putchar(тоо_утга[--урт_утга]);
        putchar('\n'); _exit(1);
    }
}
#define шалгах(нөхцөл) 검사((нөхцөл), __LINE__)

int main(int 인수개수, char **аргумент_Жагсаалт) {
    char өгөгдөл[32]; struct stat төлөв_утга;
    шалгах(인수개수 == 2 && strcmp(аргумент_Жагсаалт[1], "check") == 0 && аргумент_Жагсаалт[2] == 0);
    шалгах(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    шалгах(нээх_файл("absent", зөвхөн_унших_утга) == -1 && 오류번호 == ENOENT);
    int Файл = нээх_файл("/posix.txt", унших_бичих | 새파일만들기, 0640);
    шалгах(Файл == 3);
    шалгах(бичих_файл_өгөгдөл(Файл, "abcd", 4) == 4);
    шалгах(нээх_файл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    шалгах(파일상태읽기(Файл, &төлөв_утга) == 0 && төлөв_утга.st_size == 4 && S_ISREG(төлөв_утга.st_mode));
    шалгах((төлөв_утга.st_mode & 0777) == 0640 && төлөв_утга.st_nlink == 1);
    шалгах(хайх_файл(Файл, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Файл);
    шалгах(복제 == 4);
    шалгах(파일자료읽기(복제, өгөгдөл, 2) == 2 && memcmp(өгөгдөл, "ab", 2) == 0);
    шалгах(파일자료읽기(Файл, өгөгдөл, 2) == 2 && memcmp(өгөгдөл, "cd", 2) == 0);
    шалгах(파일자료읽기(Файл, өгөгдөл, 1) == 0);
    шалгах(fcntl(Файл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Файл, F_GETFD) == 1);
    шалгах(fcntl(복제, F_GETFD) == 0);
    шалгах(dup2(Файл, Файл) == Файл && fcntl(Файл, F_GETFD) == 1);
    шалгах(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    шалгах(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Файл, F_GETFL) & O_APPEND));
    шалгах(lseek(Файл, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Файл, 0, SEEK_CUR) == 5);
    шалгах(fcntl(Файл, F_SETFL, 0) == 0);
    шалгах(lseek(Файл, 8, SEEK_SET) == 8 && write(Файл, "Z", 1) == 1);
    шалгах(lseek(복제, 5, SEEK_SET) == 5 && read(Файл, өгөгдөл, 4) == 4);
    шалгах(өгөгдөл[0] == 0 && өгөгдөл[1] == 0 && өгөгдөл[2] == 0 && өгөгдөл[3] == 'Z');
    шалгах(ftruncate(Файл, 2) == 0 && lseek(Файл, 0, SEEK_CUR) == 9);
    шалгах(ftruncate(Файл, 6) == 0 && lseek(Файл, 2, SEEK_SET) == 2 && read(Файл, өгөгдөл, 4) == 4);
    шалгах(!өгөгдөл[0] && !өгөгдөл[1] && !өгөгдөл[2] && !өгөгдөл[3]);
    шалгах(lseek(Файл, 2147483647, SEEK_SET) == 2147483647);
    шалгах(lseek(Файл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    шалгах(lseek(Файл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    шалгах(write(Файл, "!", 1) == -1 && errno == EFBIG);
    шалгах(lseek(Файл, 0, SEEK_SET) == 0);
    шалгах(read(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    шалгах(read(Файл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    шалгах(write(Файл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    шалгах(read(Файл, өгөгдөл, (size_t)-1) == -1 && errno == EINVAL);
    шалгах(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    шалгах(fstat(Файл, (void *)0x00100000) == -1 && errno == EFAULT);
    шалгах(lseek(Файл, 0, SEEK_CUR) == 0);
    шалгах(read(Файл, NULL, 0) == 0 && write(Файл, NULL, 0) == 0);
    шалгах(арилгах_файл_оролт_нэр("posix.txt") == 0);
    шалгах(fstat(Файл, &төлөв_утга) == 0 && төлөв_утга.st_nlink == 0 && төлөв_утга.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    шалгах(새파일 == 5 && fstat(새파일, &төлөв_утга) == 0 && төлөв_утга.st_size == 0);
    шалгах(read(Файл, өгөгдөл, 2) == 2 && memcmp(өгөгдөл, "ab", 2) == 0);
    шалгах(close(Файл) == 0 && close(복제) == 0 && close(새파일) == 0);
    шалгах(close(새파일) == -1 && errno == EBADF);
    шалгах(unlink("posix.txt") == 0);
    Файл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    шалгах(Файл == 3 && fcntl(Файл, F_GETFD) == 1);
    шалгах(read(Файл, өгөгдөл, 1) == -1 && errno == EBADF);
    шалгах(write(Файл, "keep", 4) == 4);
    for (int индекс = 4; индекс < 32; индекс++) шалгах(dup(Файл) == индекс);
    шалгах(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    шалгах(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    шалгах(fstat(Файл, &төлөв_утга) == 0 && төлөв_утга.st_size == 4);
    for (int индекс = 3; индекс < 32; индекс++) шалгах(close(индекс) == 0);
    шалгах(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Файл = open("posix.txt", O_RDONLY);
    шалгах(Файл == 3 && write(Файл, өгөгдөл, 1) == -1 && errno == EBADF);
    шалгах(fcntl(Файл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    шалгах(close(8) == 0 && close(Файл) == 0 && unlink("posix.txt") == 0);
    шалгах(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    шалгах(fstat(1, &төлөв_утга) == 0 && S_ISCHR(төлөв_утга.st_mode));
    шалгах(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    шалгах(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr хаяг; char хаяг_Бичвэр[16];
    шалгах(inet_pton(AF_INET, "10.0.2.2", &хаяг) == 1 && ntohl(хаяг.s_addr) == 0x0a000202U);
    шалгах(inet_ntop(AF_INET, &хаяг, хаяг_Бичвэр, sizeof хаяг_Бичвэр) == хаяг_Бичвэр && strcmp(хаяг_Бичвэр, "10.0.2.2") == 0);
    шалгах(inet_pton(AF_INET, "256.0.0.1", &хаяг) == 0 && ntohl(хаяг.s_addr) == 0x0a000202U);
    шалгах(inet_pton(AF_INET, "01.0.0.1", &хаяг) == 0);
    шалгах(inet_ntop(AF_INET, &хаяг, хаяг_Бичвэр, 3) == NULL && errno == ENOSPC);
    шалгах(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Нэр[] = "slot0";
    for (int индекс = 0; индекс < 8; индекс++) {
        Нэр[4] = '0' + индекс;
        int 열린파일 = open(Нэр, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { шалгах(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    шалгах(개수 > 0 && 개수 < 8);
    шалгах(unlink("slot0") == 0);
    шалгах(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    шалгах(close(보관[0]) == 0);
    Файл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    шалгах(Файл >= 0 && close(Файл) == 0 && unlink("held-slot") == 0);
    for (int индекс = 1; индекс < 개수; индекс++) {
        Нэр[4] = '0' + индекс;
        шалгах(close(보관[индекс]) == 0 && unlink(Нэр) == 0);
    }
    шалгах(fsync(-1) == -1 && errno == EBADF);
    шалгах(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
