#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ngonka, int diidol) {
    검사항목수++;
    if (!ngonka) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int njuuteendi_njaru = 0;
        do { 숫자[njuuteendi_njaru++] = '0' + diidol % 10; diidol /= 10; } while (diidol);
        while (njuuteendi_njaru) putchar(숫자[--njuuteendi_njaru]);
        putchar('\n'); _exit(1);
    }
}
#define ƴeewtaade(ngonka) 검사((ngonka), __LINE__)

int main(int 인수개수, char **hujja_Doggol) {
    char keɓe[32]; struct stat ngonka_njaru;
    ƴeewtaade(인수개수 == 2 && strcmp(hujja_Doggol[1], "check") == 0 && hujja_Doggol[2] == 0);
    ƴeewtaade(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ƴeewtaade(udditde_fiilde("absent", janngotooɗo_tan_njaru) == -1 && 오류번호 == ENOENT);
    int fiilde = udditde_fiilde("/posix.txt", tar_winndu | 새파일만들기, 0640);
    ƴeewtaade(fiilde == 3);
    ƴeewtaade(winndude_fiilde_keɓe(fiilde, "abcd", 4) == 4);
    ƴeewtaade(udditde_fiilde("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ƴeewtaade(파일상태읽기(fiilde, &ngonka_njaru) == 0 && ngonka_njaru.st_size == 4 && S_ISREG(ngonka_njaru.st_mode));
    ƴeewtaade((ngonka_njaru.st_mode & 0777) == 0640 && ngonka_njaru.st_nlink == 1);
    ƴeewtaade(파일위치옮기기(fiilde, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(fiilde);
    ƴeewtaade(복제 == 4);
    ƴeewtaade(파일자료읽기(복제, keɓe, 2) == 2 && memcmp(keɓe, "ab", 2) == 0);
    ƴeewtaade(파일자료읽기(fiilde, keɓe, 2) == 2 && memcmp(keɓe, "cd", 2) == 0);
    ƴeewtaade(파일자료읽기(fiilde, keɓe, 1) == 0);
    ƴeewtaade(fcntl(fiilde, F_SETFD, FD_CLOEXEC) == 0 && fcntl(fiilde, F_GETFD) == 1);
    ƴeewtaade(fcntl(복제, F_GETFD) == 0);
    ƴeewtaade(dup2(fiilde, fiilde) == fiilde && fcntl(fiilde, F_GETFD) == 1);
    ƴeewtaade(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ƴeewtaade(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(fiilde, F_GETFL) & O_APPEND));
    ƴeewtaade(lseek(fiilde, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(fiilde, 0, SEEK_CUR) == 5);
    ƴeewtaade(fcntl(fiilde, F_SETFL, 0) == 0);
    ƴeewtaade(lseek(fiilde, 8, SEEK_SET) == 8 && write(fiilde, "Z", 1) == 1);
    ƴeewtaade(lseek(복제, 5, SEEK_SET) == 5 && read(fiilde, keɓe, 4) == 4);
    ƴeewtaade(keɓe[0] == 0 && keɓe[1] == 0 && keɓe[2] == 0 && keɓe[3] == 'Z');
    ƴeewtaade(ftruncate(fiilde, 2) == 0 && lseek(fiilde, 0, SEEK_CUR) == 9);
    ƴeewtaade(ftruncate(fiilde, 6) == 0 && lseek(fiilde, 2, SEEK_SET) == 2 && read(fiilde, keɓe, 4) == 4);
    ƴeewtaade(!keɓe[0] && !keɓe[1] && !keɓe[2] && !keɓe[3]);
    ƴeewtaade(lseek(fiilde, 2147483647, SEEK_SET) == 2147483647);
    ƴeewtaade(lseek(fiilde, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ƴeewtaade(lseek(fiilde, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ƴeewtaade(write(fiilde, "!", 1) == -1 && errno == EFBIG);
    ƴeewtaade(lseek(fiilde, 0, SEEK_SET) == 0);
    ƴeewtaade(read(fiilde, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ƴeewtaade(read(fiilde, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ƴeewtaade(write(fiilde, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ƴeewtaade(read(fiilde, keɓe, (size_t)-1) == -1 && errno == EINVAL);
    ƴeewtaade(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ƴeewtaade(fstat(fiilde, (void *)0x00100000) == -1 && errno == EFAULT);
    ƴeewtaade(lseek(fiilde, 0, SEEK_CUR) == 0);
    ƴeewtaade(read(fiilde, NULL, 0) == 0 && write(fiilde, NULL, 0) == 0);
    ƴeewtaade(ittude_fiilde_naatnugol_innde("posix.txt") == 0);
    ƴeewtaade(fstat(fiilde, &ngonka_njaru) == 0 && ngonka_njaru.st_nlink == 0 && ngonka_njaru.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ƴeewtaade(새파일 == 5 && fstat(새파일, &ngonka_njaru) == 0 && ngonka_njaru.st_size == 0);
    ƴeewtaade(read(fiilde, keɓe, 2) == 2 && memcmp(keɓe, "ab", 2) == 0);
    ƴeewtaade(close(fiilde) == 0 && close(복제) == 0 && close(새파일) == 0);
    ƴeewtaade(close(새파일) == -1 && errno == EBADF);
    ƴeewtaade(unlink("posix.txt") == 0);
    fiilde = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ƴeewtaade(fiilde == 3 && fcntl(fiilde, F_GETFD) == 1);
    ƴeewtaade(read(fiilde, keɓe, 1) == -1 && errno == EBADF);
    ƴeewtaade(write(fiilde, "keep", 4) == 4);
    for (int joopirdu = 4; joopirdu < 32; joopirdu++) ƴeewtaade(dup(fiilde) == joopirdu);
    ƴeewtaade(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ƴeewtaade(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ƴeewtaade(fstat(fiilde, &ngonka_njaru) == 0 && ngonka_njaru.st_size == 4);
    for (int joopirdu = 3; joopirdu < 32; joopirdu++) ƴeewtaade(close(joopirdu) == 0);
    ƴeewtaade(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    fiilde = open("posix.txt", O_RDONLY);
    ƴeewtaade(fiilde == 3 && write(fiilde, keɓe, 1) == -1 && errno == EBADF);
    ƴeewtaade(fcntl(fiilde, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ƴeewtaade(close(8) == 0 && close(fiilde) == 0 && unlink("posix.txt") == 0);
    ƴeewtaade(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ƴeewtaade(fstat(1, &ngonka_njaru) == 0 && S_ISCHR(ngonka_njaru.st_mode));
    ƴeewtaade(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ƴeewtaade(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ñiiɓirde; char ñiiɓirde_binndi[16];
    ƴeewtaade(inet_pton(AF_INET, "10.0.2.2", &ñiiɓirde) == 1 && ntohl(ñiiɓirde.s_addr) == 0x0a000202U);
    ƴeewtaade(inet_ntop(AF_INET, &ñiiɓirde, ñiiɓirde_binndi, sizeof ñiiɓirde_binndi) == ñiiɓirde_binndi && strcmp(ñiiɓirde_binndi, "10.0.2.2") == 0);
    ƴeewtaade(inet_pton(AF_INET, "256.0.0.1", &ñiiɓirde) == 0 && ntohl(ñiiɓirde.s_addr) == 0x0a000202U);
    ƴeewtaade(inet_pton(AF_INET, "01.0.0.1", &ñiiɓirde) == 0);
    ƴeewtaade(inet_ntop(AF_INET, &ñiiɓirde, ñiiɓirde_binndi, 3) == NULL && errno == ENOSPC);
    ƴeewtaade(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char innde[] = "slot0";
    for (int joopirdu = 0; joopirdu < 8; joopirdu++) {
        innde[4] = '0' + joopirdu;
        int 열린파일 = open(innde, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ƴeewtaade(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ƴeewtaade(개수 > 0 && 개수 < 8);
    ƴeewtaade(unlink("slot0") == 0);
    ƴeewtaade(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ƴeewtaade(close(보관[0]) == 0);
    fiilde = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ƴeewtaade(fiilde >= 0 && close(fiilde) == 0 && unlink("held-slot") == 0);
    for (int joopirdu = 1; joopirdu < 개수; joopirdu++) {
        innde[4] = '0' + joopirdu;
        ƴeewtaade(close(보관[joopirdu]) == 0 && unlink(innde) == 0);
    }
    ƴeewtaade(fsync(-1) == -1 && errno == EBADF);
    ƴeewtaade(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
