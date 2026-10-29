#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int sąlyga, int Eilutė) {
    검사항목수++;
    if (!sąlyga) {
        puts("POSIX CHECK FAILED");
        char skaitmuo_VALUE[12]; int 길이 = 0;
        do { skaitmuo_VALUE[길이++] = '0' + Eilutė % 10; Eilutė /= 10; } while (Eilutė);
        while (길이) putchar(skaitmuo_VALUE[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define patvirtinti(sąlyga) 검사((sąlyga), __LINE__)

int main(int 인수개수, char **argumentas_Sąrašas) {
    char duomenys[32]; struct stat Būsena_VALUE;
    patvirtinti(인수개수 == 2 && strcmp(argumentas_Sąrašas[1], "check") == 0 && argumentas_Sąrašas[2] == 0);
    patvirtinti(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    patvirtinti(kurti_Failas("absent", tik_skaitomas_VALUE) == -1 && klaidos_numeris == ENOENT);
    int Failas = kurti_Failas("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    patvirtinti(Failas == 3);
    patvirtinti(rašymas_Failas_duomenys(Failas, "abcd", 4) == 4);
    patvirtinti(kurti_Failas("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    patvirtinti(파일상태읽기(Failas, &Būsena_VALUE) == 0 && Būsena_VALUE.st_size == 4 && S_ISREG(Būsena_VALUE.st_mode));
    patvirtinti((Būsena_VALUE.st_mode & 0777) == 0640 && Būsena_VALUE.st_nlink == 1);
    patvirtinti(ieškoti_Failas(Failas, 0, 처음기준) == 0);
    int klonas_VALUE = 파일서술자복제(Failas);
    patvirtinti(klonas_VALUE == 4);
    patvirtinti(파일자료읽기(klonas_VALUE, duomenys, 2) == 2 && memcmp(duomenys, "ab", 2) == 0);
    patvirtinti(파일자료읽기(Failas, duomenys, 2) == 2 && memcmp(duomenys, "cd", 2) == 0);
    patvirtinti(파일자료읽기(Failas, duomenys, 1) == 0);
    patvirtinti(fcntl(Failas, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Failas, F_GETFD) == 1);
    patvirtinti(fcntl(klonas_VALUE, F_GETFD) == 0);
    patvirtinti(dup2(Failas, Failas) == Failas && fcntl(Failas, F_GETFD) == 1);
    patvirtinti(dup2(-1, klonas_VALUE) == -1 && errno == EBADF && fcntl(klonas_VALUE, F_GETFD) == 0);
    patvirtinti(fcntl(klonas_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Failas, F_GETFL) & O_APPEND));
    patvirtinti(lseek(Failas, 0, SEEK_SET) == 0 && write(klonas_VALUE, "e", 1) == 1 && lseek(Failas, 0, SEEK_CUR) == 5);
    patvirtinti(fcntl(Failas, F_SETFL, 0) == 0);
    patvirtinti(lseek(Failas, 8, SEEK_SET) == 8 && write(Failas, "Z", 1) == 1);
    patvirtinti(lseek(klonas_VALUE, 5, SEEK_SET) == 5 && read(Failas, duomenys, 4) == 4);
    patvirtinti(duomenys[0] == 0 && duomenys[1] == 0 && duomenys[2] == 0 && duomenys[3] == 'Z');
    patvirtinti(ftruncate(Failas, 2) == 0 && lseek(Failas, 0, SEEK_CUR) == 9);
    patvirtinti(ftruncate(Failas, 6) == 0 && lseek(Failas, 2, SEEK_SET) == 2 && read(Failas, duomenys, 4) == 4);
    patvirtinti(!duomenys[0] && !duomenys[1] && !duomenys[2] && !duomenys[3]);
    patvirtinti(lseek(Failas, 2147483647, SEEK_SET) == 2147483647);
    patvirtinti(lseek(Failas, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    patvirtinti(lseek(Failas, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    patvirtinti(write(Failas, "!", 1) == -1 && errno == EFBIG);
    patvirtinti(lseek(Failas, 0, SEEK_SET) == 0);
    patvirtinti(read(Failas, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    patvirtinti(read(Failas, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    patvirtinti(write(Failas, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    patvirtinti(read(Failas, duomenys, (size_t)-1) == -1 && errno == EINVAL);
    patvirtinti(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    patvirtinti(fstat(Failas, (void *)0x00100000) == -1 && errno == EFAULT);
    patvirtinti(lseek(Failas, 0, SEEK_CUR) == 0);
    patvirtinti(read(Failas, NULL, 0) == 0 && write(Failas, NULL, 0) == 0);
    patvirtinti(pašalinti_Failas_įrašas_pavadinimas("posix.txt") == 0);
    patvirtinti(fstat(Failas, &Būsena_VALUE) == 0 && Būsena_VALUE.st_nlink == 0 && Būsena_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    patvirtinti(새파일 == 5 && fstat(새파일, &Būsena_VALUE) == 0 && Būsena_VALUE.st_size == 0);
    patvirtinti(read(Failas, duomenys, 2) == 2 && memcmp(duomenys, "ab", 2) == 0);
    patvirtinti(close(Failas) == 0 && close(klonas_VALUE) == 0 && close(새파일) == 0);
    patvirtinti(close(새파일) == -1 && errno == EBADF);
    patvirtinti(unlink("posix.txt") == 0);
    Failas = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    patvirtinti(Failas == 3 && fcntl(Failas, F_GETFD) == 1);
    patvirtinti(read(Failas, duomenys, 1) == -1 && errno == EBADF);
    patvirtinti(write(Failas, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) patvirtinti(dup(Failas) == INDEX);
    patvirtinti(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    patvirtinti(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    patvirtinti(fstat(Failas, &Būsena_VALUE) == 0 && Būsena_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) patvirtinti(close(INDEX) == 0);
    patvirtinti(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Failas = open("posix.txt", O_RDONLY);
    patvirtinti(Failas == 3 && write(Failas, duomenys, 1) == -1 && errno == EBADF);
    patvirtinti(fcntl(Failas, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    patvirtinti(close(8) == 0 && close(Failas) == 0 && unlink("posix.txt") == 0);
    patvirtinti(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    patvirtinti(fstat(1, &Būsena_VALUE) == 0 && S_ISCHR(Būsena_VALUE.st_mode));
    patvirtinti(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    patvirtinti(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    patvirtinti(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    patvirtinti(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    patvirtinti(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    patvirtinti(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    patvirtinti(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    patvirtinti(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], prekė_COUNT = 0; char Pavadinimas_2[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Pavadinimas_2[4] = '0' + INDEX;
        int 열린파일 = open(Pavadinimas_2, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { patvirtinti(errno == ENOSPC); break; }
        보관[prekė_COUNT++] = 열린파일;
    }
    patvirtinti(prekė_COUNT > 0 && prekė_COUNT < 8);
    patvirtinti(unlink("slot0") == 0);
    patvirtinti(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    patvirtinti(close(보관[0]) == 0);
    Failas = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    patvirtinti(Failas >= 0 && close(Failas) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < prekė_COUNT; INDEX++) {
        Pavadinimas_2[4] = '0' + INDEX;
        patvirtinti(close(보관[INDEX]) == 0 && unlink(Pavadinimas_2) == 0);
    }
    patvirtinti(fsync(-1) == -1 && errno == EBADF);
    patvirtinti(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
