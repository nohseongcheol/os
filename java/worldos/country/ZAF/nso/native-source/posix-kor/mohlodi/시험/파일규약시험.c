#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int seemo, int mothaladi) {
    검사항목수++;
    if (!seemo) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int botelele_boleng = 0;
        do { 숫자[botelele_boleng++] = '0' + mothaladi % 10; mothaladi /= 10; } while (mothaladi);
        while (botelele_boleng) putchar(숫자[--botelele_boleng]);
        putchar('\n'); _exit(1);
    }
}
#define kgonthiša(seemo) 검사((seemo), __LINE__)

int main(int 인수개수, char **akumente_Lenaneo) {
    char data[32]; struct stat boemo_boleng;
    kgonthiša(인수개수 == 2 && strcmp(akumente_Lenaneo[1], "check") == 0 && akumente_Lenaneo[2] == 0);
    kgonthiša(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    kgonthiša(bula_faele("absent", balwago_fela_boleng) == -1 && 오류번호 == ENOENT);
    int Faele = bula_faele("/posix.txt", bala_ngwala | 새파일만들기, 0640);
    kgonthiša(Faele == 3);
    kgonthiša(ngwala_faele_data(Faele, "abcd", 4) == 4);
    kgonthiša(bula_faele("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    kgonthiša(파일상태읽기(Faele, &boemo_boleng) == 0 && boemo_boleng.st_size == 4 && S_ISREG(boemo_boleng.st_mode));
    kgonthiša((boemo_boleng.st_mode & 0777) == 0640 && boemo_boleng.st_nlink == 1);
    kgonthiša(nyaka_faele(Faele, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Faele);
    kgonthiša(복제 == 4);
    kgonthiša(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    kgonthiša(파일자료읽기(Faele, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    kgonthiša(파일자료읽기(Faele, data, 1) == 0);
    kgonthiša(fcntl(Faele, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Faele, F_GETFD) == 1);
    kgonthiša(fcntl(복제, F_GETFD) == 0);
    kgonthiša(dup2(Faele, Faele) == Faele && fcntl(Faele, F_GETFD) == 1);
    kgonthiša(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    kgonthiša(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Faele, F_GETFL) & O_APPEND));
    kgonthiša(lseek(Faele, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Faele, 0, SEEK_CUR) == 5);
    kgonthiša(fcntl(Faele, F_SETFL, 0) == 0);
    kgonthiša(lseek(Faele, 8, SEEK_SET) == 8 && write(Faele, "Z", 1) == 1);
    kgonthiša(lseek(복제, 5, SEEK_SET) == 5 && read(Faele, data, 4) == 4);
    kgonthiša(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    kgonthiša(ftruncate(Faele, 2) == 0 && lseek(Faele, 0, SEEK_CUR) == 9);
    kgonthiša(ftruncate(Faele, 6) == 0 && lseek(Faele, 2, SEEK_SET) == 2 && read(Faele, data, 4) == 4);
    kgonthiša(!data[0] && !data[1] && !data[2] && !data[3]);
    kgonthiša(lseek(Faele, 2147483647, SEEK_SET) == 2147483647);
    kgonthiša(lseek(Faele, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    kgonthiša(lseek(Faele, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    kgonthiša(write(Faele, "!", 1) == -1 && errno == EFBIG);
    kgonthiša(lseek(Faele, 0, SEEK_SET) == 0);
    kgonthiša(read(Faele, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    kgonthiša(read(Faele, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    kgonthiša(write(Faele, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    kgonthiša(read(Faele, data, (size_t)-1) == -1 && errno == EINVAL);
    kgonthiša(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    kgonthiša(fstat(Faele, (void *)0x00100000) == -1 && errno == EFAULT);
    kgonthiša(lseek(Faele, 0, SEEK_CUR) == 0);
    kgonthiša(read(Faele, NULL, 0) == 0 && write(Faele, NULL, 0) == 0);
    kgonthiša(tloša_faele_go_tsenya_tshedimošo_leina("posix.txt") == 0);
    kgonthiša(fstat(Faele, &boemo_boleng) == 0 && boemo_boleng.st_nlink == 0 && boemo_boleng.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    kgonthiša(새파일 == 5 && fstat(새파일, &boemo_boleng) == 0 && boemo_boleng.st_size == 0);
    kgonthiša(read(Faele, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    kgonthiša(close(Faele) == 0 && close(복제) == 0 && close(새파일) == 0);
    kgonthiša(close(새파일) == -1 && errno == EBADF);
    kgonthiša(unlink("posix.txt") == 0);
    Faele = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    kgonthiša(Faele == 3 && fcntl(Faele, F_GETFD) == 1);
    kgonthiša(read(Faele, data, 1) == -1 && errno == EBADF);
    kgonthiša(write(Faele, "keep", 4) == 4);
    for (int lokela = 4; lokela < 32; lokela++) kgonthiša(dup(Faele) == lokela);
    kgonthiša(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    kgonthiša(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    kgonthiša(fstat(Faele, &boemo_boleng) == 0 && boemo_boleng.st_size == 4);
    for (int lokela = 3; lokela < 32; lokela++) kgonthiša(close(lokela) == 0);
    kgonthiša(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Faele = open("posix.txt", O_RDONLY);
    kgonthiša(Faele == 3 && write(Faele, data, 1) == -1 && errno == EBADF);
    kgonthiša(fcntl(Faele, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    kgonthiša(close(8) == 0 && close(Faele) == 0 && unlink("posix.txt") == 0);
    kgonthiša(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    kgonthiša(fstat(1, &boemo_boleng) == 0 && S_ISCHR(boemo_boleng.st_mode));
    kgonthiša(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    kgonthiša(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr atrese; char atrese_SMS[16];
    kgonthiša(inet_pton(AF_INET, "10.0.2.2", &atrese) == 1 && ntohl(atrese.s_addr) == 0x0a000202U);
    kgonthiša(inet_ntop(AF_INET, &atrese, atrese_SMS, sizeof atrese_SMS) == atrese_SMS && strcmp(atrese_SMS, "10.0.2.2") == 0);
    kgonthiša(inet_pton(AF_INET, "256.0.0.1", &atrese) == 0 && ntohl(atrese.s_addr) == 0x0a000202U);
    kgonthiša(inet_pton(AF_INET, "01.0.0.1", &atrese) == 0);
    kgonthiša(inet_ntop(AF_INET, &atrese, atrese_SMS, 3) == NULL && errno == ENOSPC);
    kgonthiša(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Leina[] = "slot0";
    for (int lokela = 0; lokela < 8; lokela++) {
        Leina[4] = '0' + lokela;
        int 열린파일 = open(Leina, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { kgonthiša(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    kgonthiša(개수 > 0 && 개수 < 8);
    kgonthiša(unlink("slot0") == 0);
    kgonthiša(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    kgonthiša(close(보관[0]) == 0);
    Faele = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    kgonthiša(Faele >= 0 && close(Faele) == 0 && unlink("held-slot") == 0);
    for (int lokela = 1; lokela < 개수; lokela++) {
        Leina[4] = '0' + lokela;
        kgonthiša(close(보관[lokela]) == 0 && unlink(Leina) == 0);
    }
    kgonthiša(fsync(-1) == -1 && errno == EBADF);
    kgonthiša(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
