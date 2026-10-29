#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int պայման, int կապ) {
    검사항목수++;
    if (!պայման) {
        puts("POSIX CHECK FAILED");
        char թվանշան_արժեք[12]; int տեւողություն_արժեք = 0;
        do { թվանշան_արժեք[տեւողություն_արժեք++] = '0' + կապ % 10; կապ /= 10; } while (կապ);
        while (տեւողություն_արժեք) putchar(թվանշան_արժեք[--տեւողություն_արժեք]);
        putchar('\n'); _exit(1);
    }
}
#define հաստատել(պայման) 검사((պայման), __LINE__)

int main(int 인수개수, char **արգումենտ_Ցուցակ) {
    char տվյալ[32]; struct stat վիճակ_արժեք;
    հաստատել(인수개수 == 2 && strcmp(արգումենտ_Ցուցակ[1], "check") == 0 && արգումենտ_Ցուցակ[2] == 0);
    հաստատել(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    հաստատել(բացել_նիշք("absent", միայն_կարդալու_արժեք) == -1 && 오류번호 == ENOENT);
    int Ֆայլ = բացել_նիշք("/posix.txt", կարդալ_գրել | 새파일만들기, 0640);
    հաստատել(Ֆայլ == 3);
    հաստատել(գրել_նիշք_տվյալ(Ֆայլ, "abcd", 4) == 4);
    հաստատել(բացել_նիշք("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    հաստատել(파일상태읽기(Ֆայլ, &վիճակ_արժեք) == 0 && վիճակ_արժեք.st_size == 4 && S_ISREG(վիճակ_արժեք.st_mode));
    հաստատել((վիճակ_արժեք.st_mode & 0777) == 0640 && վիճակ_արժեք.st_nlink == 1);
    հաստատել(որոնել_նիշք(Ֆայլ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Ֆայլ);
    հաստատել(복제 == 4);
    հաստատել(파일자료읽기(복제, տվյալ, 2) == 2 && memcmp(տվյալ, "ab", 2) == 0);
    հաստատել(파일자료읽기(Ֆայլ, տվյալ, 2) == 2 && memcmp(տվյալ, "cd", 2) == 0);
    հաստատել(파일자료읽기(Ֆայլ, տվյալ, 1) == 0);
    հաստատել(fcntl(Ֆայլ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Ֆայլ, F_GETFD) == 1);
    հաստատել(fcntl(복제, F_GETFD) == 0);
    հաստատել(dup2(Ֆայլ, Ֆայլ) == Ֆայլ && fcntl(Ֆայլ, F_GETFD) == 1);
    հաստատել(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    հաստատել(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Ֆայլ, F_GETFL) & O_APPEND));
    հաստատել(lseek(Ֆայլ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Ֆայլ, 0, SEEK_CUR) == 5);
    հաստատել(fcntl(Ֆայլ, F_SETFL, 0) == 0);
    հաստատել(lseek(Ֆայլ, 8, SEEK_SET) == 8 && write(Ֆայլ, "Z", 1) == 1);
    հաստատել(lseek(복제, 5, SEEK_SET) == 5 && read(Ֆայլ, տվյալ, 4) == 4);
    հաստատել(տվյալ[0] == 0 && տվյալ[1] == 0 && տվյալ[2] == 0 && տվյալ[3] == 'Z');
    հաստատել(ftruncate(Ֆայլ, 2) == 0 && lseek(Ֆայլ, 0, SEEK_CUR) == 9);
    հաստատել(ftruncate(Ֆայլ, 6) == 0 && lseek(Ֆայլ, 2, SEEK_SET) == 2 && read(Ֆայլ, տվյալ, 4) == 4);
    հաստատել(!տվյալ[0] && !տվյալ[1] && !տվյալ[2] && !տվյալ[3]);
    հաստատել(lseek(Ֆայլ, 2147483647, SEEK_SET) == 2147483647);
    հաստատել(lseek(Ֆայլ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    հաստատել(lseek(Ֆայլ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    հաստատել(write(Ֆայլ, "!", 1) == -1 && errno == EFBIG);
    հաստատել(lseek(Ֆայլ, 0, SEEK_SET) == 0);
    հաստատել(read(Ֆայլ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    հաստատել(read(Ֆայլ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    հաստատել(write(Ֆայլ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    հաստատել(read(Ֆայլ, տվյալ, (size_t)-1) == -1 && errno == EINVAL);
    հաստատել(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    հաստատել(fstat(Ֆայլ, (void *)0x00100000) == -1 && errno == EFAULT);
    հաստատել(lseek(Ֆայլ, 0, SEEK_CUR) == 0);
    հաստատել(read(Ֆայլ, NULL, 0) == 0 && write(Ֆայլ, NULL, 0) == 0);
    հաստատել(հեռացնել_նիշք_մուտքագրում_անուն("posix.txt") == 0);
    հաստատել(fstat(Ֆայլ, &վիճակ_արժեք) == 0 && վիճակ_արժեք.st_nlink == 0 && վիճակ_արժեք.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    հաստատել(새파일 == 5 && fstat(새파일, &վիճակ_արժեք) == 0 && վիճակ_արժեք.st_size == 0);
    հաստատել(read(Ֆայլ, տվյալ, 2) == 2 && memcmp(տվյալ, "ab", 2) == 0);
    հաստատել(close(Ֆայլ) == 0 && close(복제) == 0 && close(새파일) == 0);
    հաստատել(close(새파일) == -1 && errno == EBADF);
    հաստատել(unlink("posix.txt") == 0);
    Ֆայլ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    հաստատել(Ֆայլ == 3 && fcntl(Ֆայլ, F_GETFD) == 1);
    հաստատել(read(Ֆայլ, տվյալ, 1) == -1 && errno == EBADF);
    հաստատել(write(Ֆայլ, "keep", 4) == 4);
    for (int դասիչ = 4; դասիչ < 32; դասիչ++) հաստատել(dup(Ֆայլ) == դասիչ);
    հաստատել(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    հաստատել(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    հաստատել(fstat(Ֆայլ, &վիճակ_արժեք) == 0 && վիճակ_արժեք.st_size == 4);
    for (int դասիչ = 3; դասիչ < 32; դասիչ++) հաստատել(close(դասիչ) == 0);
    հաստատել(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Ֆայլ = open("posix.txt", O_RDONLY);
    հաստատել(Ֆայլ == 3 && write(Ֆայլ, տվյալ, 1) == -1 && errno == EBADF);
    հաստատել(fcntl(Ֆայլ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    հաստատել(close(8) == 0 && close(Ֆայլ) == 0 && unlink("posix.txt") == 0);
    հաստատել(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    հաստատել(fstat(1, &վիճակ_արժեք) == 0 && S_ISCHR(վիճակ_արժեք.st_mode));
    հաստատել(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    հաստատել(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr հասցե; char հասցե_Գրվածք[16];
    հաստատել(inet_pton(AF_INET, "10.0.2.2", &հասցե) == 1 && ntohl(հասցե.s_addr) == 0x0a000202U);
    հաստատել(inet_ntop(AF_INET, &հասցե, հասցե_Գրվածք, sizeof հասցե_Գրվածք) == հասցե_Գրվածք && strcmp(հասցե_Գրվածք, "10.0.2.2") == 0);
    հաստատել(inet_pton(AF_INET, "256.0.0.1", &հասցե) == 0 && ntohl(հասցե.s_addr) == 0x0a000202U);
    հաստատել(inet_pton(AF_INET, "01.0.0.1", &հասցե) == 0);
    հաստատել(inet_ntop(AF_INET, &հասցե, հասցե_Գրվածք, 3) == NULL && errno == ENOSPC);
    հաստատել(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Անուն[] = "slot0";
    for (int դասիչ = 0; դասիչ < 8; դասիչ++) {
        Անուն[4] = '0' + դասիչ;
        int 열린파일 = open(Անուն, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { հաստատել(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    հաստատել(개수 > 0 && 개수 < 8);
    հաստատել(unlink("slot0") == 0);
    հաստատել(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    հաստատել(close(보관[0]) == 0);
    Ֆայլ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    հաստատել(Ֆայլ >= 0 && close(Ֆայլ) == 0 && unlink("held-slot") == 0);
    for (int դասիչ = 1; դասիչ < 개수; դասիչ++) {
        Անուն[4] = '0' + դասիչ;
        հաստատել(close(보관[դասիչ]) == 0 && unlink(Անուն) == 0);
    }
    հաստատել(fsync(-1) == -1 && errno == EBADF);
    հաստատել(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
