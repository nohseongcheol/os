#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int anam, int buum) {
    검사항목수++;
    if (!anam) {
        puts("POSIX CHECK FAILED");
        char siifar_xëyma[12]; int diir_xëyma = 0;
        do { siifar_xëyma[diir_xëyma++] = '0' + buum % 10; buum /= 10; } while (buum);
        while (diir_xëyma) putchar(siifar_xëyma[--diir_xëyma]);
        putchar('\n'); _exit(1);
    }
}
#define luñutu(anam) 검사((anam), __LINE__)

int main(int 인수개수, char **Tegtal_lim) {
    char mbir[32]; struct stat nekkin_xëyma;
    luñutu(인수개수 == 2 && strcmp(Tegtal_lim[1], "check") == 0 && Tegtal_lim[2] == 0);
    luñutu(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    luñutu(sos_bara_denc("absent", ngir_jaŋarek_la_xëyma) == -1 && 오류번호 == ENOENT);
    int bara_denc = sos_bara_denc("/posix.txt", jàng_bind | 새파일만들기, 0640);
    luñutu(bara_denc == 3);
    luñutu(biir_bara_denc_mbir(bara_denc, "abcd", 4) == 4);
    luñutu(sos_bara_denc("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    luñutu(파일상태읽기(bara_denc, &nekkin_xëyma) == 0 && nekkin_xëyma.st_size == 4 && S_ISREG(nekkin_xëyma.st_mode));
    luñutu((nekkin_xëyma.st_mode & 0777) == 0640 && nekkin_xëyma.st_nlink == 1);
    luñutu(seet_bara_denc(bara_denc, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(bara_denc);
    luñutu(복제 == 4);
    luñutu(파일자료읽기(복제, mbir, 2) == 2 && memcmp(mbir, "ab", 2) == 0);
    luñutu(파일자료읽기(bara_denc, mbir, 2) == 2 && memcmp(mbir, "cd", 2) == 0);
    luñutu(파일자료읽기(bara_denc, mbir, 1) == 0);
    luñutu(fcntl(bara_denc, F_SETFD, FD_CLOEXEC) == 0 && fcntl(bara_denc, F_GETFD) == 1);
    luñutu(fcntl(복제, F_GETFD) == 0);
    luñutu(dup2(bara_denc, bara_denc) == bara_denc && fcntl(bara_denc, F_GETFD) == 1);
    luñutu(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    luñutu(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(bara_denc, F_GETFL) & O_APPEND));
    luñutu(lseek(bara_denc, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(bara_denc, 0, SEEK_CUR) == 5);
    luñutu(fcntl(bara_denc, F_SETFL, 0) == 0);
    luñutu(lseek(bara_denc, 8, SEEK_SET) == 8 && write(bara_denc, "Z", 1) == 1);
    luñutu(lseek(복제, 5, SEEK_SET) == 5 && read(bara_denc, mbir, 4) == 4);
    luñutu(mbir[0] == 0 && mbir[1] == 0 && mbir[2] == 0 && mbir[3] == 'Z');
    luñutu(ftruncate(bara_denc, 2) == 0 && lseek(bara_denc, 0, SEEK_CUR) == 9);
    luñutu(ftruncate(bara_denc, 6) == 0 && lseek(bara_denc, 2, SEEK_SET) == 2 && read(bara_denc, mbir, 4) == 4);
    luñutu(!mbir[0] && !mbir[1] && !mbir[2] && !mbir[3]);
    luñutu(lseek(bara_denc, 2147483647, SEEK_SET) == 2147483647);
    luñutu(lseek(bara_denc, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    luñutu(lseek(bara_denc, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    luñutu(write(bara_denc, "!", 1) == -1 && errno == EFBIG);
    luñutu(lseek(bara_denc, 0, SEEK_SET) == 0);
    luñutu(read(bara_denc, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    luñutu(read(bara_denc, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    luñutu(write(bara_denc, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    luñutu(read(bara_denc, mbir, (size_t)-1) == -1 && errno == EINVAL);
    luñutu(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    luñutu(fstat(bara_denc, (void *)0x00100000) == -1 && errno == EFAULT);
    luñutu(lseek(bara_denc, 0, SEEK_CUR) == 0);
    luñutu(read(bara_denc, NULL, 0) == 0 && write(bara_denc, NULL, 0) == 0);
    luñutu(dandal_bara_denc_dugal_xabaar_tur("posix.txt") == 0);
    luñutu(fstat(bara_denc, &nekkin_xëyma) == 0 && nekkin_xëyma.st_nlink == 0 && nekkin_xëyma.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    luñutu(새파일 == 5 && fstat(새파일, &nekkin_xëyma) == 0 && nekkin_xëyma.st_size == 0);
    luñutu(read(bara_denc, mbir, 2) == 2 && memcmp(mbir, "ab", 2) == 0);
    luñutu(close(bara_denc) == 0 && close(복제) == 0 && close(새파일) == 0);
    luñutu(close(새파일) == -1 && errno == EBADF);
    luñutu(unlink("posix.txt") == 0);
    bara_denc = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    luñutu(bara_denc == 3 && fcntl(bara_denc, F_GETFD) == 1);
    luñutu(read(bara_denc, mbir, 1) == -1 && errno == EBADF);
    luñutu(write(bara_denc, "keep", 4) == 4);
    for (int àlluwa_tur = 4; àlluwa_tur < 32; àlluwa_tur++) luñutu(dup(bara_denc) == àlluwa_tur);
    luñutu(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    luñutu(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    luñutu(fstat(bara_denc, &nekkin_xëyma) == 0 && nekkin_xëyma.st_size == 4);
    for (int àlluwa_tur = 3; àlluwa_tur < 32; àlluwa_tur++) luñutu(close(àlluwa_tur) == 0);
    luñutu(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    bara_denc = open("posix.txt", O_RDONLY);
    luñutu(bara_denc == 3 && write(bara_denc, mbir, 1) == -1 && errno == EBADF);
    luñutu(fcntl(bara_denc, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    luñutu(close(8) == 0 && close(bara_denc) == 0 && unlink("posix.txt") == 0);
    luñutu(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    luñutu(fstat(1, &nekkin_xëyma) == 0 && S_ISCHR(nekkin_xëyma.st_mode));
    luñutu(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    luñutu(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr dëkkuwaay; char dëkkuwaay_SMS[16];
    luñutu(inet_pton(AF_INET, "10.0.2.2", &dëkkuwaay) == 1 && ntohl(dëkkuwaay.s_addr) == 0x0a000202U);
    luñutu(inet_ntop(AF_INET, &dëkkuwaay, dëkkuwaay_SMS, sizeof dëkkuwaay_SMS) == dëkkuwaay_SMS && strcmp(dëkkuwaay_SMS, "10.0.2.2") == 0);
    luñutu(inet_pton(AF_INET, "256.0.0.1", &dëkkuwaay) == 0 && ntohl(dëkkuwaay.s_addr) == 0x0a000202U);
    luñutu(inet_pton(AF_INET, "01.0.0.1", &dëkkuwaay) == 0);
    luñutu(inet_ntop(AF_INET, &dëkkuwaay, dëkkuwaay_SMS, 3) == NULL && errno == ENOSPC);
    luñutu(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char tur_253d1510[] = "slot0";
    for (int àlluwa_tur = 0; àlluwa_tur < 8; àlluwa_tur++) {
        tur_253d1510[4] = '0' + àlluwa_tur;
        int 열린파일 = open(tur_253d1510, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { luñutu(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    luñutu(개수 > 0 && 개수 < 8);
    luñutu(unlink("slot0") == 0);
    luñutu(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    luñutu(close(보관[0]) == 0);
    bara_denc = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    luñutu(bara_denc >= 0 && close(bara_denc) == 0 && unlink("held-slot") == 0);
    for (int àlluwa_tur = 1; àlluwa_tur < 개수; àlluwa_tur++) {
        tur_253d1510[4] = '0' + àlluwa_tur;
        luñutu(close(보관[àlluwa_tur]) == 0 && unlink(tur_253d1510) == 0);
    }
    luñutu(fsync(-1) == -1 && errno == EBADF);
    luñutu(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
