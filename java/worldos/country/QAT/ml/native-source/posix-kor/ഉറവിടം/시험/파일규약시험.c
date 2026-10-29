#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int അവസ്ഥ, int ലൈൻ) {
    검사항목수++;
    if (!അവസ്ഥ) {
        puts("POSIX CHECK FAILED");
        char അക്കം_മൂല്യം[12]; int ദൈര്_ഘ്യം_മൂല്യം = 0;
        do { അക്കം_മൂല്യം[ദൈര്_ഘ്യം_മൂല്യം++] = '0' + ലൈൻ % 10; ലൈൻ /= 10; } while (ലൈൻ);
        while (ദൈര്_ഘ്യം_മൂല്യം) putchar(അക്കം_മൂല്യം[--ദൈര്_ഘ്യം_മൂല്യം]);
        putchar('\n'); _exit(1);
    }
}
#define പരിശോധിക്കുക(അവസ്ഥ) 검사((അവസ്ഥ), __LINE__)

int main(int 인수개수, char **ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്) {
    char ഡാറ്റാ[32]; struct stat അവസ്ഥ_മൂല്യം;
    പരിശോധിക്കുക(인수개수 == 2 && strcmp(ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്[1], "check") == 0 && ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്[2] == 0);
    പരിശോധിക്കുക(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    പരിശോധിക്കുക(തുറക്കുക_ഫയല്("absent", വായന_മാത്രം_മൂല്യം) == -1 && 오류번호 == ENOENT);
    int ഫയല് = തുറക്കുക_ഫയല്("/posix.txt", വായനാ_റൈറ്റ് | 새파일만들기, 0640);
    പരിശോധിക്കുക(ഫയല് == 3);
    പരിശോധിക്കുക(റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(ഫയല്, "abcd", 4) == 4);
    പരിശോധിക്കുക(തുറക്കുക_ഫയല്("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    പരിശോധിക്കുക(파일상태읽기(ഫയല്, &അവസ്ഥ_മൂല്യം) == 0 && അവസ്ഥ_മൂല്യം.st_size == 4 && S_ISREG(അവസ്ഥ_മൂല്യം.st_mode));
    പരിശോധിക്കുക((അവസ്ഥ_മൂല്യം.st_mode & 0777) == 0640 && അവസ്ഥ_മൂല്യം.st_nlink == 1);
    പരിശോധിക്കുക(തിരയുക_ഫയല്(ഫയല്, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ഫയല്);
    പരിശോധിക്കുക(복제 == 4);
    പരിശോധിക്കുക(파일자료읽기(복제, ഡാറ്റാ, 2) == 2 && memcmp(ഡാറ്റാ, "ab", 2) == 0);
    പരിശോധിക്കുക(파일자료읽기(ഫയല്, ഡാറ്റാ, 2) == 2 && memcmp(ഡാറ്റാ, "cd", 2) == 0);
    പരിശോധിക്കുക(파일자료읽기(ഫയല്, ഡാറ്റാ, 1) == 0);
    പരിശോധിക്കുക(fcntl(ഫയല്, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ഫയല്, F_GETFD) == 1);
    പരിശോധിക്കുക(fcntl(복제, F_GETFD) == 0);
    പരിശോധിക്കുക(dup2(ഫയല്, ഫയല്) == ഫയല് && fcntl(ഫയല്, F_GETFD) == 1);
    പരിശോധിക്കുക(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    പരിശോധിക്കുക(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ഫയല്, F_GETFL) & O_APPEND));
    പരിശോധിക്കുക(lseek(ഫയല്, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ഫയല്, 0, SEEK_CUR) == 5);
    പരിശോധിക്കുക(fcntl(ഫയല്, F_SETFL, 0) == 0);
    പരിശോധിക്കുക(lseek(ഫയല്, 8, SEEK_SET) == 8 && write(ഫയല്, "Z", 1) == 1);
    പരിശോധിക്കുക(lseek(복제, 5, SEEK_SET) == 5 && read(ഫയല്, ഡാറ്റാ, 4) == 4);
    പരിശോധിക്കുക(ഡാറ്റാ[0] == 0 && ഡാറ്റാ[1] == 0 && ഡാറ്റാ[2] == 0 && ഡാറ്റാ[3] == 'Z');
    പരിശോധിക്കുക(ftruncate(ഫയല്, 2) == 0 && lseek(ഫയല്, 0, SEEK_CUR) == 9);
    പരിശോധിക്കുക(ftruncate(ഫയല്, 6) == 0 && lseek(ഫയല്, 2, SEEK_SET) == 2 && read(ഫയല്, ഡാറ്റാ, 4) == 4);
    പരിശോധിക്കുക(!ഡാറ്റാ[0] && !ഡാറ്റാ[1] && !ഡാറ്റാ[2] && !ഡാറ്റാ[3]);
    പരിശോധിക്കുക(lseek(ഫയല്, 2147483647, SEEK_SET) == 2147483647);
    പരിശോധിക്കുക(lseek(ഫയല്, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    പരിശോധിക്കുക(lseek(ഫയല്, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    പരിശോധിക്കുക(write(ഫയല്, "!", 1) == -1 && errno == EFBIG);
    പരിശോധിക്കുക(lseek(ഫയല്, 0, SEEK_SET) == 0);
    പരിശോധിക്കുക(read(ഫയല്, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    പരിശോധിക്കുക(read(ഫയല്, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    പരിശോധിക്കുക(write(ഫയല്, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    പരിശോധിക്കുക(read(ഫയല്, ഡാറ്റാ, (size_t)-1) == -1 && errno == EINVAL);
    പരിശോധിക്കുക(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    പരിശോധിക്കുക(fstat(ഫയല്, (void *)0x00100000) == -1 && errno == EFAULT);
    പരിശോധിക്കുക(lseek(ഫയല്, 0, SEEK_CUR) == 0);
    പരിശോധിക്കുക(read(ഫയല്, NULL, 0) == 0 && write(ഫയല്, NULL, 0) == 0);
    പരിശോധിക്കുക(നീക്കംചെയ്യുക_ഫയല്_എന്_ട്രി_നാ_മം("posix.txt") == 0);
    പരിശോധിക്കുക(fstat(ഫയല്, &അവസ്ഥ_മൂല്യം) == 0 && അവസ്ഥ_മൂല്യം.st_nlink == 0 && അവസ്ഥ_മൂല്യം.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    പരിശോധിക്കുക(새파일 == 5 && fstat(새파일, &അവസ്ഥ_മൂല്യം) == 0 && അവസ്ഥ_മൂല്യം.st_size == 0);
    പരിശോധിക്കുക(read(ഫയല്, ഡാറ്റാ, 2) == 2 && memcmp(ഡാറ്റാ, "ab", 2) == 0);
    പരിശോധിക്കുക(close(ഫയല്) == 0 && close(복제) == 0 && close(새파일) == 0);
    പരിശോധിക്കുക(close(새파일) == -1 && errno == EBADF);
    പരിശോധിക്കുക(unlink("posix.txt") == 0);
    ഫയല് = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    പരിശോധിക്കുക(ഫയല് == 3 && fcntl(ഫയല്, F_GETFD) == 1);
    പരിശോധിക്കുക(read(ഫയല്, ഡാറ്റാ, 1) == -1 && errno == EBADF);
    പരിശോധിക്കുക(write(ഫയല്, "keep", 4) == 4);
    for (int സൂചിക = 4; സൂചിക < 32; സൂചിക++) പരിശോധിക്കുക(dup(ഫയല്) == സൂചിക);
    പരിശോധിക്കുക(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    പരിശോധിക്കുക(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    പരിശോധിക്കുക(fstat(ഫയല്, &അവസ്ഥ_മൂല്യം) == 0 && അവസ്ഥ_മൂല്യം.st_size == 4);
    for (int സൂചിക = 3; സൂചിക < 32; സൂചിക++) പരിശോധിക്കുക(close(സൂചിക) == 0);
    പരിശോധിക്കുക(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ഫയല് = open("posix.txt", O_RDONLY);
    പരിശോധിക്കുക(ഫയല് == 3 && write(ഫയല്, ഡാറ്റാ, 1) == -1 && errno == EBADF);
    പരിശോധിക്കുക(fcntl(ഫയല്, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    പരിശോധിക്കുക(close(8) == 0 && close(ഫയല്) == 0 && unlink("posix.txt") == 0);
    പരിശോധിക്കുക(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    പരിശോധിക്കുക(fstat(1, &അവസ്ഥ_മൂല്യം) == 0 && S_ISCHR(അവസ്ഥ_മൂല്യം.st_mode));
    പരിശോധിക്കുക(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    പരിശോധിക്കുക(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ഇമെയിൽ; char ഇമെയിൽ_ലിഖിതം[16];
    പരിശോധിക്കുക(inet_pton(AF_INET, "10.0.2.2", &ഇമെയിൽ) == 1 && ntohl(ഇമെയിൽ.s_addr) == 0x0a000202U);
    പരിശോധിക്കുക(inet_ntop(AF_INET, &ഇമെയിൽ, ഇമെയിൽ_ലിഖിതം, sizeof ഇമെയിൽ_ലിഖിതം) == ഇമെയിൽ_ലിഖിതം && strcmp(ഇമെയിൽ_ലിഖിതം, "10.0.2.2") == 0);
    പരിശോധിക്കുക(inet_pton(AF_INET, "256.0.0.1", &ഇമെയിൽ) == 0 && ntohl(ഇമെയിൽ.s_addr) == 0x0a000202U);
    പരിശോധിക്കുക(inet_pton(AF_INET, "01.0.0.1", &ഇമെയിൽ) == 0);
    പരിശോധിക്കുക(inet_ntop(AF_INET, &ഇമെയിൽ, ഇമെയിൽ_ലിഖിതം, 3) == NULL && errno == ENOSPC);
    പരിശോധിക്കുക(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char പേരു്[] = "slot0";
    for (int സൂചിക = 0; സൂചിക < 8; സൂചിക++) {
        പേരു്[4] = '0' + സൂചിക;
        int 열린파일 = open(പേരു്, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { പരിശോധിക്കുക(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    പരിശോധിക്കുക(개수 > 0 && 개수 < 8);
    പരിശോധിക്കുക(unlink("slot0") == 0);
    പരിശോധിക്കുക(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    പരിശോധിക്കുക(close(보관[0]) == 0);
    ഫയല് = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    പരിശോധിക്കുക(ഫയല് >= 0 && close(ഫയല്) == 0 && unlink("held-slot") == 0);
    for (int സൂചിക = 1; സൂചിക < 개수; സൂചിക++) {
        പേരു്[4] = '0' + സൂചിക;
        പരിശോധിക്കുക(close(보관[സൂചിക]) == 0 && unlink(പേരു്) == 0);
    }
    പരിശോധിക്കുക(fsync(-1) == -1 && errno == EBADF);
    പരിശോധിക്കുക(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
