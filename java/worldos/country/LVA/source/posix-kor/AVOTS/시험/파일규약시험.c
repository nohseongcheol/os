#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int nosacījums, int Līniju) {
    검사항목수++;
    if (!nosacījums) {
        puts("POSIX CHECK FAILED");
        char cipars_VALUE[12]; int 길이 = 0;
        do { cipars_VALUE[길이++] = '0' + Līniju % 10; Līniju /= 10; } while (Līniju);
        while (길이) putchar(cipars_VALUE[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define verificēt(nosacījums) 검사((nosacījums), __LINE__)

int main(int 인수개수, char **arg_Saraksts) {
    char dati[32]; struct stat Statuss_VALUE;
    verificēt(인수개수 == 2 && strcmp(arg_Saraksts[1], "check") == 0 && arg_Saraksts[2] == 0);
    verificēt(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verificēt(atvērt_Fails("absent", tikai_lasāms_VALUE) == -1 && kļūdas_numurs == ENOENT);
    int Fails = atvērt_Fails("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    verificēt(Fails == 3);
    verificēt(rakstīšana_Fails_dati(Fails, "abcd", 4) == 4);
    verificēt(atvērt_Fails("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verificēt(파일상태읽기(Fails, &Statuss_VALUE) == 0 && Statuss_VALUE.st_size == 4 && S_ISREG(Statuss_VALUE.st_mode));
    verificēt((Statuss_VALUE.st_mode & 0777) == 0640 && Statuss_VALUE.st_nlink == 1);
    verificēt(meklēt_Fails(Fails, 0, 처음기준) == 0);
    int klons_VALUE = 파일서술자복제(Fails);
    verificēt(klons_VALUE == 4);
    verificēt(파일자료읽기(klons_VALUE, dati, 2) == 2 && memcmp(dati, "ab", 2) == 0);
    verificēt(파일자료읽기(Fails, dati, 2) == 2 && memcmp(dati, "cd", 2) == 0);
    verificēt(파일자료읽기(Fails, dati, 1) == 0);
    verificēt(fcntl(Fails, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fails, F_GETFD) == 1);
    verificēt(fcntl(klons_VALUE, F_GETFD) == 0);
    verificēt(dup2(Fails, Fails) == Fails && fcntl(Fails, F_GETFD) == 1);
    verificēt(dup2(-1, klons_VALUE) == -1 && errno == EBADF && fcntl(klons_VALUE, F_GETFD) == 0);
    verificēt(fcntl(klons_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Fails, F_GETFL) & O_APPEND));
    verificēt(lseek(Fails, 0, SEEK_SET) == 0 && write(klons_VALUE, "e", 1) == 1 && lseek(Fails, 0, SEEK_CUR) == 5);
    verificēt(fcntl(Fails, F_SETFL, 0) == 0);
    verificēt(lseek(Fails, 8, SEEK_SET) == 8 && write(Fails, "Z", 1) == 1);
    verificēt(lseek(klons_VALUE, 5, SEEK_SET) == 5 && read(Fails, dati, 4) == 4);
    verificēt(dati[0] == 0 && dati[1] == 0 && dati[2] == 0 && dati[3] == 'Z');
    verificēt(ftruncate(Fails, 2) == 0 && lseek(Fails, 0, SEEK_CUR) == 9);
    verificēt(ftruncate(Fails, 6) == 0 && lseek(Fails, 2, SEEK_SET) == 2 && read(Fails, dati, 4) == 4);
    verificēt(!dati[0] && !dati[1] && !dati[2] && !dati[3]);
    verificēt(lseek(Fails, 2147483647, SEEK_SET) == 2147483647);
    verificēt(lseek(Fails, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verificēt(lseek(Fails, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verificēt(write(Fails, "!", 1) == -1 && errno == EFBIG);
    verificēt(lseek(Fails, 0, SEEK_SET) == 0);
    verificēt(read(Fails, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificēt(read(Fails, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verificēt(write(Fails, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verificēt(read(Fails, dati, (size_t)-1) == -1 && errno == EINVAL);
    verificēt(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verificēt(fstat(Fails, (void *)0x00100000) == -1 && errno == EFAULT);
    verificēt(lseek(Fails, 0, SEEK_CUR) == 0);
    verificēt(read(Fails, NULL, 0) == 0 && write(Fails, NULL, 0) == 0);
    verificēt(noņemt_Fails_ievade_nosaukums("posix.txt") == 0);
    verificēt(fstat(Fails, &Statuss_VALUE) == 0 && Statuss_VALUE.st_nlink == 0 && Statuss_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificēt(새파일 == 5 && fstat(새파일, &Statuss_VALUE) == 0 && Statuss_VALUE.st_size == 0);
    verificēt(read(Fails, dati, 2) == 2 && memcmp(dati, "ab", 2) == 0);
    verificēt(close(Fails) == 0 && close(klons_VALUE) == 0 && close(새파일) == 0);
    verificēt(close(새파일) == -1 && errno == EBADF);
    verificēt(unlink("posix.txt") == 0);
    Fails = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verificēt(Fails == 3 && fcntl(Fails, F_GETFD) == 1);
    verificēt(read(Fails, dati, 1) == -1 && errno == EBADF);
    verificēt(write(Fails, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verificēt(dup(Fails) == INDEX);
    verificēt(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verificēt(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verificēt(fstat(Fails, &Statuss_VALUE) == 0 && Statuss_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verificēt(close(INDEX) == 0);
    verificēt(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fails = open("posix.txt", O_RDONLY);
    verificēt(Fails == 3 && write(Fails, dati, 1) == -1 && errno == EBADF);
    verificēt(fcntl(Fails, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verificēt(close(8) == 0 && close(Fails) == 0 && unlink("posix.txt") == 0);
    verificēt(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verificēt(fstat(1, &Statuss_VALUE) == 0 && S_ISCHR(Statuss_VALUE.st_mode));
    verificēt(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verificēt(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adrese; char adrese_SMS[16];
    verificēt(inet_pton(AF_INET, "10.0.2.2", &adrese) == 1 && ntohl(adrese.s_addr) == 0x0a000202U);
    verificēt(inet_ntop(AF_INET, &adrese, adrese_SMS, sizeof adrese_SMS) == adrese_SMS && strcmp(adrese_SMS, "10.0.2.2") == 0);
    verificēt(inet_pton(AF_INET, "256.0.0.1", &adrese) == 0 && ntohl(adrese.s_addr) == 0x0a000202U);
    verificēt(inet_pton(AF_INET, "01.0.0.1", &adrese) == 0);
    verificēt(inet_ntop(AF_INET, &adrese, adrese_SMS, 3) == NULL && errno == ENOSPC);
    verificēt(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], krājums_COUNT = 0; char Nosaukums[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nosaukums[4] = '0' + INDEX;
        int 열린파일 = open(Nosaukums, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verificēt(errno == ENOSPC); break; }
        보관[krājums_COUNT++] = 열린파일;
    }
    verificēt(krājums_COUNT > 0 && krājums_COUNT < 8);
    verificēt(unlink("slot0") == 0);
    verificēt(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verificēt(close(보관[0]) == 0);
    Fails = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verificēt(Fails >= 0 && close(Fails) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < krājums_COUNT; INDEX++) {
        Nosaukums[4] = '0' + INDEX;
        verificēt(close(보관[INDEX]) == 0 && unlink(Nosaukums) == 0);
    }
    verificēt(fsync(-1) == -1 && errno == EBADF);
    verificēt(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
