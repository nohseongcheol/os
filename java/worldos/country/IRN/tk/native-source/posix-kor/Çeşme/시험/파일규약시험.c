#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int şert, int setir) {
    검사항목수++;
    if (!şert) {
        puts("POSIX CHECK FAILED");
        char san_baha[12]; int dowamlylyk_baha = 0;
        do { san_baha[dowamlylyk_baha++] = '0' + setir % 10; setir /= 10; } while (setir);
        while (dowamlylyk_baha) putchar(san_baha[--dowamlylyk_baha]);
        putchar('\n'); _exit(1);
    }
}
#define barla(şert) 검사((şert), __LINE__)

int main(int 인수개수, char **argument_Sanaw) {
    char maglumat[32]; struct stat ýagdaý_baha;
    barla(인수개수 == 2 && strcmp(argument_Sanaw[1], "check") == 0 && argument_Sanaw[2] == 0);
    barla(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    barla(aç_faýl("absent", diňe_okalýan_baha) == -1 && 오류번호 == ENOENT);
    int Faýl = aç_faýl("/posix.txt", okalýan_ýazylýan | 새파일만들기, 0640);
    barla(Faýl == 3);
    barla(ýaz_faýl_maglumat(Faýl, "abcd", 4) == 4);
    barla(aç_faýl("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    barla(파일상태읽기(Faýl, &ýagdaý_baha) == 0 && ýagdaý_baha.st_size == 4 && S_ISREG(ýagdaý_baha.st_mode));
    barla((ýagdaý_baha.st_mode & 0777) == 0640 && ýagdaý_baha.st_nlink == 1);
    barla(gözle_faýl(Faýl, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Faýl);
    barla(복제 == 4);
    barla(파일자료읽기(복제, maglumat, 2) == 2 && memcmp(maglumat, "ab", 2) == 0);
    barla(파일자료읽기(Faýl, maglumat, 2) == 2 && memcmp(maglumat, "cd", 2) == 0);
    barla(파일자료읽기(Faýl, maglumat, 1) == 0);
    barla(fcntl(Faýl, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Faýl, F_GETFD) == 1);
    barla(fcntl(복제, F_GETFD) == 0);
    barla(dup2(Faýl, Faýl) == Faýl && fcntl(Faýl, F_GETFD) == 1);
    barla(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    barla(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Faýl, F_GETFL) & O_APPEND));
    barla(lseek(Faýl, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Faýl, 0, SEEK_CUR) == 5);
    barla(fcntl(Faýl, F_SETFL, 0) == 0);
    barla(lseek(Faýl, 8, SEEK_SET) == 8 && write(Faýl, "Z", 1) == 1);
    barla(lseek(복제, 5, SEEK_SET) == 5 && read(Faýl, maglumat, 4) == 4);
    barla(maglumat[0] == 0 && maglumat[1] == 0 && maglumat[2] == 0 && maglumat[3] == 'Z');
    barla(ftruncate(Faýl, 2) == 0 && lseek(Faýl, 0, SEEK_CUR) == 9);
    barla(ftruncate(Faýl, 6) == 0 && lseek(Faýl, 2, SEEK_SET) == 2 && read(Faýl, maglumat, 4) == 4);
    barla(!maglumat[0] && !maglumat[1] && !maglumat[2] && !maglumat[3]);
    barla(lseek(Faýl, 2147483647, SEEK_SET) == 2147483647);
    barla(lseek(Faýl, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    barla(lseek(Faýl, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    barla(write(Faýl, "!", 1) == -1 && errno == EFBIG);
    barla(lseek(Faýl, 0, SEEK_SET) == 0);
    barla(read(Faýl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    barla(read(Faýl, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    barla(write(Faýl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    barla(read(Faýl, maglumat, (size_t)-1) == -1 && errno == EINVAL);
    barla(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    barla(fstat(Faýl, (void *)0x00100000) == -1 && errno == EFAULT);
    barla(lseek(Faýl, 0, SEEK_CUR) == 0);
    barla(read(Faýl, NULL, 0) == 0 && write(Faýl, NULL, 0) == 0);
    barla(aýyr_faýl_girizmeklik_at("posix.txt") == 0);
    barla(fstat(Faýl, &ýagdaý_baha) == 0 && ýagdaý_baha.st_nlink == 0 && ýagdaý_baha.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    barla(새파일 == 5 && fstat(새파일, &ýagdaý_baha) == 0 && ýagdaý_baha.st_size == 0);
    barla(read(Faýl, maglumat, 2) == 2 && memcmp(maglumat, "ab", 2) == 0);
    barla(close(Faýl) == 0 && close(복제) == 0 && close(새파일) == 0);
    barla(close(새파일) == -1 && errno == EBADF);
    barla(unlink("posix.txt") == 0);
    Faýl = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    barla(Faýl == 3 && fcntl(Faýl, F_GETFD) == 1);
    barla(read(Faýl, maglumat, 1) == -1 && errno == EBADF);
    barla(write(Faýl, "keep", 4) == 4);
    for (int indeks = 4; indeks < 32; indeks++) barla(dup(Faýl) == indeks);
    barla(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    barla(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    barla(fstat(Faýl, &ýagdaý_baha) == 0 && ýagdaý_baha.st_size == 4);
    for (int indeks = 3; indeks < 32; indeks++) barla(close(indeks) == 0);
    barla(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Faýl = open("posix.txt", O_RDONLY);
    barla(Faýl == 3 && write(Faýl, maglumat, 1) == -1 && errno == EBADF);
    barla(fcntl(Faýl, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    barla(close(8) == 0 && close(Faýl) == 0 && unlink("posix.txt") == 0);
    barla(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    barla(fstat(1, &ýagdaý_baha) == 0 && S_ISCHR(ýagdaý_baha.st_mode));
    barla(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    barla(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr salgy; char salgy_SMS[16];
    barla(inet_pton(AF_INET, "10.0.2.2", &salgy) == 1 && ntohl(salgy.s_addr) == 0x0a000202U);
    barla(inet_ntop(AF_INET, &salgy, salgy_SMS, sizeof salgy_SMS) == salgy_SMS && strcmp(salgy_SMS, "10.0.2.2") == 0);
    barla(inet_pton(AF_INET, "256.0.0.1", &salgy) == 0 && ntohl(salgy.s_addr) == 0x0a000202U);
    barla(inet_pton(AF_INET, "01.0.0.1", &salgy) == 0);
    barla(inet_ntop(AF_INET, &salgy, salgy_SMS, 3) == NULL && errno == ENOSPC);
    barla(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Ad[] = "slot0";
    for (int indeks = 0; indeks < 8; indeks++) {
        Ad[4] = '0' + indeks;
        int 열린파일 = open(Ad, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { barla(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    barla(개수 > 0 && 개수 < 8);
    barla(unlink("slot0") == 0);
    barla(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    barla(close(보관[0]) == 0);
    Faýl = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    barla(Faýl >= 0 && close(Faýl) == 0 && unlink("held-slot") == 0);
    for (int indeks = 1; indeks < 개수; indeks++) {
        Ad[4] = '0' + indeks;
        barla(close(보관[indeks]) == 0 && unlink(Ad) == 0);
    }
    barla(fsync(-1) == -1 && errno == EBADF);
    barla(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
