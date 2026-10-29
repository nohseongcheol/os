#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int icyangombwa, int umurongo) {
    검사항목수++;
    if (!icyangombwa) {
        puts("POSIX CHECK FAILED");
        char umubare_agaciro[12]; int uburebure_agaciro = 0;
        do { umubare_agaciro[uburebure_agaciro++] = '0' + umurongo % 10; umurongo /= 10; } while (umurongo);
        while (uburebure_agaciro) putchar(umubare_agaciro[--uburebure_agaciro]);
        putchar('\n'); _exit(1);
    }
}
#define gusuzuma(icyangombwa) 검사((icyangombwa), __LINE__)

int main(int 인수개수, char **ingingo_Urutonde) {
    char amakurushingiro[32]; struct stat imimerere_agaciro;
    gusuzuma(인수개수 == 2 && strcmp(ingingo_Urutonde[1], "check") == 0 && ingingo_Urutonde[2] == 0);
    gusuzuma(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    gusuzuma(kurema_dosiye("absent", soma_gusa_agaciro) == -1 && 오류번호 == ENOENT);
    int Idosiye = kurema_dosiye("/posix.txt", gusoma_kwandika | 새파일만들기, 0640);
    gusuzuma(Idosiye == 3);
    gusuzuma(kwandika_dosiye_amakurushingiro(Idosiye, "abcd", 4) == 4);
    gusuzuma(kurema_dosiye("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    gusuzuma(파일상태읽기(Idosiye, &imimerere_agaciro) == 0 && imimerere_agaciro.st_size == 4 && S_ISREG(imimerere_agaciro.st_mode));
    gusuzuma((imimerere_agaciro.st_mode & 0777) == 0640 && imimerere_agaciro.st_nlink == 1);
    gusuzuma(파일위치옮기기(Idosiye, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Idosiye);
    gusuzuma(복제 == 4);
    gusuzuma(파일자료읽기(복제, amakurushingiro, 2) == 2 && memcmp(amakurushingiro, "ab", 2) == 0);
    gusuzuma(파일자료읽기(Idosiye, amakurushingiro, 2) == 2 && memcmp(amakurushingiro, "cd", 2) == 0);
    gusuzuma(파일자료읽기(Idosiye, amakurushingiro, 1) == 0);
    gusuzuma(fcntl(Idosiye, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Idosiye, F_GETFD) == 1);
    gusuzuma(fcntl(복제, F_GETFD) == 0);
    gusuzuma(dup2(Idosiye, Idosiye) == Idosiye && fcntl(Idosiye, F_GETFD) == 1);
    gusuzuma(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    gusuzuma(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Idosiye, F_GETFL) & O_APPEND));
    gusuzuma(lseek(Idosiye, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Idosiye, 0, SEEK_CUR) == 5);
    gusuzuma(fcntl(Idosiye, F_SETFL, 0) == 0);
    gusuzuma(lseek(Idosiye, 8, SEEK_SET) == 8 && write(Idosiye, "Z", 1) == 1);
    gusuzuma(lseek(복제, 5, SEEK_SET) == 5 && read(Idosiye, amakurushingiro, 4) == 4);
    gusuzuma(amakurushingiro[0] == 0 && amakurushingiro[1] == 0 && amakurushingiro[2] == 0 && amakurushingiro[3] == 'Z');
    gusuzuma(ftruncate(Idosiye, 2) == 0 && lseek(Idosiye, 0, SEEK_CUR) == 9);
    gusuzuma(ftruncate(Idosiye, 6) == 0 && lseek(Idosiye, 2, SEEK_SET) == 2 && read(Idosiye, amakurushingiro, 4) == 4);
    gusuzuma(!amakurushingiro[0] && !amakurushingiro[1] && !amakurushingiro[2] && !amakurushingiro[3]);
    gusuzuma(lseek(Idosiye, 2147483647, SEEK_SET) == 2147483647);
    gusuzuma(lseek(Idosiye, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    gusuzuma(lseek(Idosiye, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    gusuzuma(write(Idosiye, "!", 1) == -1 && errno == EFBIG);
    gusuzuma(lseek(Idosiye, 0, SEEK_SET) == 0);
    gusuzuma(read(Idosiye, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    gusuzuma(read(Idosiye, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    gusuzuma(write(Idosiye, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    gusuzuma(read(Idosiye, amakurushingiro, (size_t)-1) == -1 && errno == EINVAL);
    gusuzuma(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    gusuzuma(fstat(Idosiye, (void *)0x00100000) == -1 && errno == EFAULT);
    gusuzuma(lseek(Idosiye, 0, SEEK_CUR) == 0);
    gusuzuma(read(Idosiye, NULL, 0) == 0 && write(Idosiye, NULL, 0) == 0);
    gusuzuma(gukuramo_dosiye_icyinjizwa_izina("posix.txt") == 0);
    gusuzuma(fstat(Idosiye, &imimerere_agaciro) == 0 && imimerere_agaciro.st_nlink == 0 && imimerere_agaciro.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    gusuzuma(새파일 == 5 && fstat(새파일, &imimerere_agaciro) == 0 && imimerere_agaciro.st_size == 0);
    gusuzuma(read(Idosiye, amakurushingiro, 2) == 2 && memcmp(amakurushingiro, "ab", 2) == 0);
    gusuzuma(close(Idosiye) == 0 && close(복제) == 0 && close(새파일) == 0);
    gusuzuma(close(새파일) == -1 && errno == EBADF);
    gusuzuma(unlink("posix.txt") == 0);
    Idosiye = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    gusuzuma(Idosiye == 3 && fcntl(Idosiye, F_GETFD) == 1);
    gusuzuma(read(Idosiye, amakurushingiro, 1) == -1 && errno == EBADF);
    gusuzuma(write(Idosiye, "keep", 4) == 4);
    for (int umugerekashakiro = 4; umugerekashakiro < 32; umugerekashakiro++) gusuzuma(dup(Idosiye) == umugerekashakiro);
    gusuzuma(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    gusuzuma(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    gusuzuma(fstat(Idosiye, &imimerere_agaciro) == 0 && imimerere_agaciro.st_size == 4);
    for (int umugerekashakiro = 3; umugerekashakiro < 32; umugerekashakiro++) gusuzuma(close(umugerekashakiro) == 0);
    gusuzuma(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Idosiye = open("posix.txt", O_RDONLY);
    gusuzuma(Idosiye == 3 && write(Idosiye, amakurushingiro, 1) == -1 && errno == EBADF);
    gusuzuma(fcntl(Idosiye, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    gusuzuma(close(8) == 0 && close(Idosiye) == 0 && unlink("posix.txt") == 0);
    gusuzuma(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    gusuzuma(fstat(1, &imimerere_agaciro) == 0 && S_ISCHR(imimerere_agaciro.st_mode));
    gusuzuma(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    gusuzuma(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr aderesi; char aderesi_SMS[16];
    gusuzuma(inet_pton(AF_INET, "10.0.2.2", &aderesi) == 1 && ntohl(aderesi.s_addr) == 0x0a000202U);
    gusuzuma(inet_ntop(AF_INET, &aderesi, aderesi_SMS, sizeof aderesi_SMS) == aderesi_SMS && strcmp(aderesi_SMS, "10.0.2.2") == 0);
    gusuzuma(inet_pton(AF_INET, "256.0.0.1", &aderesi) == 0 && ntohl(aderesi.s_addr) == 0x0a000202U);
    gusuzuma(inet_pton(AF_INET, "01.0.0.1", &aderesi) == 0);
    gusuzuma(inet_ntop(AF_INET, &aderesi, aderesi_SMS, 3) == NULL && errno == ENOSPC);
    gusuzuma(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Izina[] = "slot0";
    for (int umugerekashakiro = 0; umugerekashakiro < 8; umugerekashakiro++) {
        Izina[4] = '0' + umugerekashakiro;
        int 열린파일 = open(Izina, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { gusuzuma(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    gusuzuma(개수 > 0 && 개수 < 8);
    gusuzuma(unlink("slot0") == 0);
    gusuzuma(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    gusuzuma(close(보관[0]) == 0);
    Idosiye = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    gusuzuma(Idosiye >= 0 && close(Idosiye) == 0 && unlink("held-slot") == 0);
    for (int umugerekashakiro = 1; umugerekashakiro < 개수; umugerekashakiro++) {
        Izina[4] = '0' + umugerekashakiro;
        gusuzuma(close(보관[umugerekashakiro]) == 0 && unlink(Izina) == 0);
    }
    gusuzuma(fsync(-1) == -1 && errno == EBADF);
    gusuzuma(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
