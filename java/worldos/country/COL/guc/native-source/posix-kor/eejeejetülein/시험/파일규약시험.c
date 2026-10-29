#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int mülein, int liinia) {
    검사항목수++;
    if (!mülein) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int akaliaa_ajutuu = 0;
        do { 숫자[akaliaa_ajutuu++] = '0' + liinia % 10; liinia /= 10; } while (liinia);
        while (akaliaa_ajutuu) putchar(숫자[--akaliaa_ajutuu]);
        putchar('\n'); _exit(1);
    }
}
#define 확인(mülein) 검사((mülein), __LINE__)

int main(int 인수개수, char **인수목록) {
    char atijaaya[32]; struct stat jamakua_iparülein_ajutuu;
    확인(인수개수 == 2 && strcmp(인수목록[1], "check") == 0 && 인수목록[2] == 0);
    확인(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    확인(파일열기("absent", 읽기전용) == -1 && 오류번호 == ENOENT);
    int anaajaalaa = 파일열기("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    확인(anaajaalaa == 3);
    확인(ashajaa_anaajaalaa_atijaaya(anaajaalaa, "abcd", 4) == 4);
    확인(파일열기("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    확인(파일상태읽기(anaajaalaa, &jamakua_iparülein_ajutuu) == 0 && jamakua_iparülein_ajutuu.st_size == 4 && S_ISREG(jamakua_iparülein_ajutuu.st_mode));
    확인((jamakua_iparülein_ajutuu.st_mode & 0777) == 0640 && jamakua_iparülein_ajutuu.st_nlink == 1);
    확인(파일위치옮기기(anaajaalaa, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(anaajaalaa);
    확인(복제 == 4);
    확인(파일자료읽기(복제, atijaaya, 2) == 2 && memcmp(atijaaya, "ab", 2) == 0);
    확인(파일자료읽기(anaajaalaa, atijaaya, 2) == 2 && memcmp(atijaaya, "cd", 2) == 0);
    확인(파일자료읽기(anaajaalaa, atijaaya, 1) == 0);
    확인(fcntl(anaajaalaa, F_SETFD, FD_CLOEXEC) == 0 && fcntl(anaajaalaa, F_GETFD) == 1);
    확인(fcntl(복제, F_GETFD) == 0);
    확인(dup2(anaajaalaa, anaajaalaa) == anaajaalaa && fcntl(anaajaalaa, F_GETFD) == 1);
    확인(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    확인(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(anaajaalaa, F_GETFL) & O_APPEND));
    확인(lseek(anaajaalaa, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(anaajaalaa, 0, SEEK_CUR) == 5);
    확인(fcntl(anaajaalaa, F_SETFL, 0) == 0);
    확인(lseek(anaajaalaa, 8, SEEK_SET) == 8 && write(anaajaalaa, "Z", 1) == 1);
    확인(lseek(복제, 5, SEEK_SET) == 5 && read(anaajaalaa, atijaaya, 4) == 4);
    확인(atijaaya[0] == 0 && atijaaya[1] == 0 && atijaaya[2] == 0 && atijaaya[3] == 'Z');
    확인(ftruncate(anaajaalaa, 2) == 0 && lseek(anaajaalaa, 0, SEEK_CUR) == 9);
    확인(ftruncate(anaajaalaa, 6) == 0 && lseek(anaajaalaa, 2, SEEK_SET) == 2 && read(anaajaalaa, atijaaya, 4) == 4);
    확인(!atijaaya[0] && !atijaaya[1] && !atijaaya[2] && !atijaaya[3]);
    확인(lseek(anaajaalaa, 2147483647, SEEK_SET) == 2147483647);
    확인(lseek(anaajaalaa, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    확인(lseek(anaajaalaa, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    확인(write(anaajaalaa, "!", 1) == -1 && errno == EFBIG);
    확인(lseek(anaajaalaa, 0, SEEK_SET) == 0);
    확인(read(anaajaalaa, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(anaajaalaa, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    확인(write(anaajaalaa, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(anaajaalaa, atijaaya, (size_t)-1) == -1 && errno == EINVAL);
    확인(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    확인(fstat(anaajaalaa, (void *)0x00100000) == -1 && errno == EFAULT);
    확인(lseek(anaajaalaa, 0, SEEK_CUR) == 0);
    확인(read(anaajaalaa, NULL, 0) == 0 && write(anaajaalaa, NULL, 0) == 0);
    확인(파일이름지우기("posix.txt") == 0);
    확인(fstat(anaajaalaa, &jamakua_iparülein_ajutuu) == 0 && jamakua_iparülein_ajutuu.st_nlink == 0 && jamakua_iparülein_ajutuu.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(새파일 == 5 && fstat(새파일, &jamakua_iparülein_ajutuu) == 0 && jamakua_iparülein_ajutuu.st_size == 0);
    확인(read(anaajaalaa, atijaaya, 2) == 2 && memcmp(atijaaya, "ab", 2) == 0);
    확인(close(anaajaalaa) == 0 && close(복제) == 0 && close(새파일) == 0);
    확인(close(새파일) == -1 && errno == EBADF);
    확인(unlink("posix.txt") == 0);
    anaajaalaa = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    확인(anaajaalaa == 3 && fcntl(anaajaalaa, F_GETFD) == 1);
    확인(read(anaajaalaa, atijaaya, 1) == -1 && errno == EBADF);
    확인(write(anaajaalaa, "keep", 4) == 4);
    for (int ee_iyatialujuna = 4; ee_iyatialujuna < 32; ee_iyatialujuna++) 확인(dup(anaajaalaa) == ee_iyatialujuna);
    확인(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    확인(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    확인(fstat(anaajaalaa, &jamakua_iparülein_ajutuu) == 0 && jamakua_iparülein_ajutuu.st_size == 4);
    for (int ee_iyatialujuna = 3; ee_iyatialujuna < 32; ee_iyatialujuna++) 확인(close(ee_iyatialujuna) == 0);
    확인(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    anaajaalaa = open("posix.txt", O_RDONLY);
    확인(anaajaalaa == 3 && write(anaajaalaa, atijaaya, 1) == -1 && errno == EBADF);
    확인(fcntl(anaajaalaa, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    확인(close(8) == 0 && close(anaajaalaa) == 0 && unlink("posix.txt") == 0);
    확인(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    확인(fstat(1, &jamakua_iparülein_ajutuu) == 0 && S_ISCHR(jamakua_iparülein_ajutuu.st_mode));
    확인(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    확인(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ejepüsee; char 주소글[16];
    확인(inet_pton(AF_INET, "10.0.2.2", &ejepüsee) == 1 && ntohl(ejepüsee.s_addr) == 0x0a000202U);
    확인(inet_ntop(AF_INET, &ejepüsee, 주소글, sizeof 주소글) == 주소글 && strcmp(주소글, "10.0.2.2") == 0);
    확인(inet_pton(AF_INET, "256.0.0.1", &ejepüsee) == 0 && ntohl(ejepüsee.s_addr) == 0x0a000202U);
    확인(inet_pton(AF_INET, "01.0.0.1", &ejepüsee) == 0);
    확인(inet_ntop(AF_INET, &ejepüsee, 주소글, 3) == NULL && errno == ENOSPC);
    확인(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char 이름[] = "slot0";
    for (int ee_iyatialujuna = 0; ee_iyatialujuna < 8; ee_iyatialujuna++) {
        이름[4] = '0' + ee_iyatialujuna;
        int 열린파일 = open(이름, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { 확인(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    확인(개수 > 0 && 개수 < 8);
    확인(unlink("slot0") == 0);
    확인(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    확인(close(보관[0]) == 0);
    anaajaalaa = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(anaajaalaa >= 0 && close(anaajaalaa) == 0 && unlink("held-slot") == 0);
    for (int ee_iyatialujuna = 1; ee_iyatialujuna < 개수; ee_iyatialujuna++) {
        이름[4] = '0' + ee_iyatialujuna;
        확인(close(보관[ee_iyatialujuna]) == 0 && unlink(이름) == 0);
    }
    확인(fsync(-1) == -1 && errno == EBADF);
    확인(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
