#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int skilyrði, int Lína) {
    검사항목수++;
    if (!skilyrði) {
        puts("POSIX CHECK FAILED");
        char tölustafur_VALUE[12]; int lengd_VALUE = 0;
        do { tölustafur_VALUE[lengd_VALUE++] = '0' + Lína % 10; Lína /= 10; } while (Lína);
        while (lengd_VALUE) putchar(tölustafur_VALUE[--lengd_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define sannprófa(skilyrði) 검사((skilyrði), __LINE__)

int main(int 인수개수, char **frumbreyta_Listi) {
    char gögn[32]; struct stat staða_VALUE_e10195a1;
    sannprófa(인수개수 == 2 && strcmp(frumbreyta_Listi[1], "check") == 0 && frumbreyta_Listi[2] == 0);
    sannprófa(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    sannprófa(opið_skrá("absent", skrifvarið_VALUE) == -1 && villa_númer == ENOENT);
    int Skrá = opið_skrá("/posix.txt", les_skrifheimild | 새파일만들기, 0640);
    sannprófa(Skrá == 3);
    sannprófa(skrifa_skrá_gögn(Skrá, "abcd", 4) == 4);
    sannprófa(opið_skrá("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    sannprófa(파일상태읽기(Skrá, &staða_VALUE_e10195a1) == 0 && staða_VALUE_e10195a1.st_size == 4 && S_ISREG(staða_VALUE_e10195a1.st_mode));
    sannprófa((staða_VALUE_e10195a1.st_mode & 0777) == 0640 && staða_VALUE_e10195a1.st_nlink == 1);
    sannprófa(leita_skrá(Skrá, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Skrá);
    sannprófa(복제 == 4);
    sannprófa(파일자료읽기(복제, gögn, 2) == 2 && memcmp(gögn, "ab", 2) == 0);
    sannprófa(파일자료읽기(Skrá, gögn, 2) == 2 && memcmp(gögn, "cd", 2) == 0);
    sannprófa(파일자료읽기(Skrá, gögn, 1) == 0);
    sannprófa(fcntl(Skrá, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Skrá, F_GETFD) == 1);
    sannprófa(fcntl(복제, F_GETFD) == 0);
    sannprófa(dup2(Skrá, Skrá) == Skrá && fcntl(Skrá, F_GETFD) == 1);
    sannprófa(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    sannprófa(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Skrá, F_GETFL) & O_APPEND));
    sannprófa(lseek(Skrá, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Skrá, 0, SEEK_CUR) == 5);
    sannprófa(fcntl(Skrá, F_SETFL, 0) == 0);
    sannprófa(lseek(Skrá, 8, SEEK_SET) == 8 && write(Skrá, "Z", 1) == 1);
    sannprófa(lseek(복제, 5, SEEK_SET) == 5 && read(Skrá, gögn, 4) == 4);
    sannprófa(gögn[0] == 0 && gögn[1] == 0 && gögn[2] == 0 && gögn[3] == 'Z');
    sannprófa(ftruncate(Skrá, 2) == 0 && lseek(Skrá, 0, SEEK_CUR) == 9);
    sannprófa(ftruncate(Skrá, 6) == 0 && lseek(Skrá, 2, SEEK_SET) == 2 && read(Skrá, gögn, 4) == 4);
    sannprófa(!gögn[0] && !gögn[1] && !gögn[2] && !gögn[3]);
    sannprófa(lseek(Skrá, 2147483647, SEEK_SET) == 2147483647);
    sannprófa(lseek(Skrá, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    sannprófa(lseek(Skrá, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    sannprófa(write(Skrá, "!", 1) == -1 && errno == EFBIG);
    sannprófa(lseek(Skrá, 0, SEEK_SET) == 0);
    sannprófa(read(Skrá, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    sannprófa(read(Skrá, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    sannprófa(write(Skrá, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    sannprófa(read(Skrá, gögn, (size_t)-1) == -1 && errno == EINVAL);
    sannprófa(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    sannprófa(fstat(Skrá, (void *)0x00100000) == -1 && errno == EFAULT);
    sannprófa(lseek(Skrá, 0, SEEK_CUR) == 0);
    sannprófa(read(Skrá, NULL, 0) == 0 && write(Skrá, NULL, 0) == 0);
    sannprófa(fjarlægja_skrá_færsla_heiti("posix.txt") == 0);
    sannprófa(fstat(Skrá, &staða_VALUE_e10195a1) == 0 && staða_VALUE_e10195a1.st_nlink == 0 && staða_VALUE_e10195a1.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    sannprófa(새파일 == 5 && fstat(새파일, &staða_VALUE_e10195a1) == 0 && staða_VALUE_e10195a1.st_size == 0);
    sannprófa(read(Skrá, gögn, 2) == 2 && memcmp(gögn, "ab", 2) == 0);
    sannprófa(close(Skrá) == 0 && close(복제) == 0 && close(새파일) == 0);
    sannprófa(close(새파일) == -1 && errno == EBADF);
    sannprófa(unlink("posix.txt") == 0);
    Skrá = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    sannprófa(Skrá == 3 && fcntl(Skrá, F_GETFD) == 1);
    sannprófa(read(Skrá, gögn, 1) == -1 && errno == EBADF);
    sannprófa(write(Skrá, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) sannprófa(dup(Skrá) == INDEX);
    sannprófa(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    sannprófa(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    sannprófa(fstat(Skrá, &staða_VALUE_e10195a1) == 0 && staða_VALUE_e10195a1.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) sannprófa(close(INDEX) == 0);
    sannprófa(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Skrá = open("posix.txt", O_RDONLY);
    sannprófa(Skrá == 3 && write(Skrá, gögn, 1) == -1 && errno == EBADF);
    sannprófa(fcntl(Skrá, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    sannprófa(close(8) == 0 && close(Skrá) == 0 && unlink("posix.txt") == 0);
    sannprófa(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    sannprófa(fstat(1, &staða_VALUE_e10195a1) == 0 && S_ISCHR(staða_VALUE_e10195a1.st_mode));
    sannprófa(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    sannprófa(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr slóð; char slóð_SMS[16];
    sannprófa(inet_pton(AF_INET, "10.0.2.2", &slóð) == 1 && ntohl(slóð.s_addr) == 0x0a000202U);
    sannprófa(inet_ntop(AF_INET, &slóð, slóð_SMS, sizeof slóð_SMS) == slóð_SMS && strcmp(slóð_SMS, "10.0.2.2") == 0);
    sannprófa(inet_pton(AF_INET, "256.0.0.1", &slóð) == 0 && ntohl(slóð.s_addr) == 0x0a000202U);
    sannprófa(inet_pton(AF_INET, "01.0.0.1", &slóð) == 0);
    sannprófa(inet_ntop(AF_INET, &slóð, slóð_SMS, 3) == NULL && errno == ENOSPC);
    sannprófa(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], vara_COUNT = 0; char Heiti[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Heiti[4] = '0' + INDEX;
        int 열린파일 = open(Heiti, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { sannprófa(errno == ENOSPC); break; }
        보관[vara_COUNT++] = 열린파일;
    }
    sannprófa(vara_COUNT > 0 && vara_COUNT < 8);
    sannprófa(unlink("slot0") == 0);
    sannprófa(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    sannprófa(close(보관[0]) == 0);
    Skrá = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    sannprófa(Skrá >= 0 && close(Skrá) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < vara_COUNT; INDEX++) {
        Heiti[4] = '0' + INDEX;
        sannprófa(close(보관[INDEX]) == 0 && unlink(Heiti) == 0);
    }
    sannprófa(fsync(-1) == -1 && errno == EBADF);
    sannprófa(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
