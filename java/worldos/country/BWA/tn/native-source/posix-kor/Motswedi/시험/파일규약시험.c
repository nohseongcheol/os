#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int boemo, int Mola) {
    검사항목수++;
    if (!boemo) {
        puts("POSIX CHECK FAILED");
        char dijite_Boleng[12]; int boleele_Boleng = 0;
        do { dijite_Boleng[boleele_Boleng++] = '0' + Mola % 10; Mola /= 10; } while (Mola);
        while (boleele_Boleng) putchar(dijite_Boleng[--boleele_Boleng]);
        putchar('\n'); _exit(1);
    }
}
#define netefatsa(boemo) 검사((boemo), __LINE__)

int main(int 인수개수, char **Thulaganyo_lenaane) {
    char tshedimosetso[32]; struct stat kemo_Boleng;
    netefatsa(인수개수 == 2 && strcmp(Thulaganyo_lenaane[1], "check") == 0 && Thulaganyo_lenaane[2] == 0);
    netefatsa(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    netefatsa(bula_faele("absent", puiso_fela_Boleng) == -1 && 오류번호 == ENOENT);
    int faele = bula_faele("/posix.txt", buisa_kwala | 새파일만들기, 0640);
    netefatsa(faele == 3);
    netefatsa(kwala_faele_tshedimosetso(faele, "abcd", 4) == 4);
    netefatsa(bula_faele("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    netefatsa(파일상태읽기(faele, &kemo_Boleng) == 0 && kemo_Boleng.st_size == 4 && S_ISREG(kemo_Boleng.st_mode));
    netefatsa((kemo_Boleng.st_mode & 0777) == 0640 && kemo_Boleng.st_nlink == 1);
    netefatsa(batla_faele(faele, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(faele);
    netefatsa(복제 == 4);
    netefatsa(파일자료읽기(복제, tshedimosetso, 2) == 2 && memcmp(tshedimosetso, "ab", 2) == 0);
    netefatsa(파일자료읽기(faele, tshedimosetso, 2) == 2 && memcmp(tshedimosetso, "cd", 2) == 0);
    netefatsa(파일자료읽기(faele, tshedimosetso, 1) == 0);
    netefatsa(fcntl(faele, F_SETFD, FD_CLOEXEC) == 0 && fcntl(faele, F_GETFD) == 1);
    netefatsa(fcntl(복제, F_GETFD) == 0);
    netefatsa(dup2(faele, faele) == faele && fcntl(faele, F_GETFD) == 1);
    netefatsa(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    netefatsa(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(faele, F_GETFL) & O_APPEND));
    netefatsa(lseek(faele, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(faele, 0, SEEK_CUR) == 5);
    netefatsa(fcntl(faele, F_SETFL, 0) == 0);
    netefatsa(lseek(faele, 8, SEEK_SET) == 8 && write(faele, "Z", 1) == 1);
    netefatsa(lseek(복제, 5, SEEK_SET) == 5 && read(faele, tshedimosetso, 4) == 4);
    netefatsa(tshedimosetso[0] == 0 && tshedimosetso[1] == 0 && tshedimosetso[2] == 0 && tshedimosetso[3] == 'Z');
    netefatsa(ftruncate(faele, 2) == 0 && lseek(faele, 0, SEEK_CUR) == 9);
    netefatsa(ftruncate(faele, 6) == 0 && lseek(faele, 2, SEEK_SET) == 2 && read(faele, tshedimosetso, 4) == 4);
    netefatsa(!tshedimosetso[0] && !tshedimosetso[1] && !tshedimosetso[2] && !tshedimosetso[3]);
    netefatsa(lseek(faele, 2147483647, SEEK_SET) == 2147483647);
    netefatsa(lseek(faele, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    netefatsa(lseek(faele, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    netefatsa(write(faele, "!", 1) == -1 && errno == EFBIG);
    netefatsa(lseek(faele, 0, SEEK_SET) == 0);
    netefatsa(read(faele, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    netefatsa(read(faele, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    netefatsa(write(faele, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    netefatsa(read(faele, tshedimosetso, (size_t)-1) == -1 && errno == EINVAL);
    netefatsa(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    netefatsa(fstat(faele, (void *)0x00100000) == -1 && errno == EFAULT);
    netefatsa(lseek(faele, 0, SEEK_CUR) == 0);
    netefatsa(read(faele, NULL, 0) == 0 && write(faele, NULL, 0) == 0);
    netefatsa(tlosa_faele_tsenyo_leina("posix.txt") == 0);
    netefatsa(fstat(faele, &kemo_Boleng) == 0 && kemo_Boleng.st_nlink == 0 && kemo_Boleng.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    netefatsa(새파일 == 5 && fstat(새파일, &kemo_Boleng) == 0 && kemo_Boleng.st_size == 0);
    netefatsa(read(faele, tshedimosetso, 2) == 2 && memcmp(tshedimosetso, "ab", 2) == 0);
    netefatsa(close(faele) == 0 && close(복제) == 0 && close(새파일) == 0);
    netefatsa(close(새파일) == -1 && errno == EBADF);
    netefatsa(unlink("posix.txt") == 0);
    faele = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    netefatsa(faele == 3 && fcntl(faele, F_GETFD) == 1);
    netefatsa(read(faele, tshedimosetso, 1) == -1 && errno == EBADF);
    netefatsa(write(faele, "keep", 4) == 4);
    for (int tshupane = 4; tshupane < 32; tshupane++) netefatsa(dup(faele) == tshupane);
    netefatsa(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    netefatsa(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    netefatsa(fstat(faele, &kemo_Boleng) == 0 && kemo_Boleng.st_size == 4);
    for (int tshupane = 3; tshupane < 32; tshupane++) netefatsa(close(tshupane) == 0);
    netefatsa(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    faele = open("posix.txt", O_RDONLY);
    netefatsa(faele == 3 && write(faele, tshedimosetso, 1) == -1 && errno == EBADF);
    netefatsa(fcntl(faele, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    netefatsa(close(8) == 0 && close(faele) == 0 && unlink("posix.txt") == 0);
    netefatsa(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    netefatsa(fstat(1, &kemo_Boleng) == 0 && S_ISCHR(kemo_Boleng.st_mode));
    netefatsa(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    netefatsa(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr aterese; char aterese_SMS[16];
    netefatsa(inet_pton(AF_INET, "10.0.2.2", &aterese) == 1 && ntohl(aterese.s_addr) == 0x0a000202U);
    netefatsa(inet_ntop(AF_INET, &aterese, aterese_SMS, sizeof aterese_SMS) == aterese_SMS && strcmp(aterese_SMS, "10.0.2.2") == 0);
    netefatsa(inet_pton(AF_INET, "256.0.0.1", &aterese) == 0 && ntohl(aterese.s_addr) == 0x0a000202U);
    netefatsa(inet_pton(AF_INET, "01.0.0.1", &aterese) == 0);
    netefatsa(inet_ntop(AF_INET, &aterese, aterese_SMS, 3) == NULL && errno == ENOSPC);
    netefatsa(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char leina[] = "slot0";
    for (int tshupane = 0; tshupane < 8; tshupane++) {
        leina[4] = '0' + tshupane;
        int 열린파일 = open(leina, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { netefatsa(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    netefatsa(개수 > 0 && 개수 < 8);
    netefatsa(unlink("slot0") == 0);
    netefatsa(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    netefatsa(close(보관[0]) == 0);
    faele = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    netefatsa(faele >= 0 && close(faele) == 0 && unlink("held-slot") == 0);
    for (int tshupane = 1; tshupane < 개수; tshupane++) {
        leina[4] = '0' + tshupane;
        netefatsa(close(보관[tshupane]) == 0 && unlink(leina) == 0);
    }
    netefatsa(fsync(-1) == -1 && errno == EBADF);
    netefatsa(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
