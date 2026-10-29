#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int sharti, int laini) {
    검사항목수++;
    if (!sharti) {
        puts("POSIX CHECK FAILED");
        char dijiti_thamani[12]; int urefu_thamani = 0;
        do { dijiti_thamani[urefu_thamani++] = '0' + laini % 10; laini /= 10; } while (laini);
        while (urefu_thamani) putchar(dijiti_thamani[--urefu_thamani]);
        putchar('\n'); _exit(1);
    }
}
#define thibitisha(sharti) 검사((sharti), __LINE__)

int main(int 인수개수, char **hoja_Orodha) {
    char data[32]; struct stat hali_thamani;
    thibitisha(인수개수 == 2 && strcmp(hoja_Orodha[1], "check") == 0 && hoja_Orodha[2] == 0);
    thibitisha(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    thibitisha(unda_faili("absent", soma_tu_thamani) == -1 && 오류번호 == ENOENT);
    int faili = unda_faili("/posix.txt", soma_andika | 새파일만들기, 0640);
    thibitisha(faili == 3);
    thibitisha(andika_faili_data(faili, "abcd", 4) == 4);
    thibitisha(unda_faili("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    thibitisha(파일상태읽기(faili, &hali_thamani) == 0 && hali_thamani.st_size == 4 && S_ISREG(hali_thamani.st_mode));
    thibitisha((hali_thamani.st_mode & 0777) == 0640 && hali_thamani.st_nlink == 1);
    thibitisha(tafuta_faili(faili, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(faili);
    thibitisha(복제 == 4);
    thibitisha(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    thibitisha(파일자료읽기(faili, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    thibitisha(파일자료읽기(faili, data, 1) == 0);
    thibitisha(fcntl(faili, F_SETFD, FD_CLOEXEC) == 0 && fcntl(faili, F_GETFD) == 1);
    thibitisha(fcntl(복제, F_GETFD) == 0);
    thibitisha(dup2(faili, faili) == faili && fcntl(faili, F_GETFD) == 1);
    thibitisha(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    thibitisha(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(faili, F_GETFL) & O_APPEND));
    thibitisha(lseek(faili, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(faili, 0, SEEK_CUR) == 5);
    thibitisha(fcntl(faili, F_SETFL, 0) == 0);
    thibitisha(lseek(faili, 8, SEEK_SET) == 8 && write(faili, "Z", 1) == 1);
    thibitisha(lseek(복제, 5, SEEK_SET) == 5 && read(faili, data, 4) == 4);
    thibitisha(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    thibitisha(ftruncate(faili, 2) == 0 && lseek(faili, 0, SEEK_CUR) == 9);
    thibitisha(ftruncate(faili, 6) == 0 && lseek(faili, 2, SEEK_SET) == 2 && read(faili, data, 4) == 4);
    thibitisha(!data[0] && !data[1] && !data[2] && !data[3]);
    thibitisha(lseek(faili, 2147483647, SEEK_SET) == 2147483647);
    thibitisha(lseek(faili, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    thibitisha(lseek(faili, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    thibitisha(write(faili, "!", 1) == -1 && errno == EFBIG);
    thibitisha(lseek(faili, 0, SEEK_SET) == 0);
    thibitisha(read(faili, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    thibitisha(read(faili, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    thibitisha(write(faili, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    thibitisha(read(faili, data, (size_t)-1) == -1 && errno == EINVAL);
    thibitisha(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    thibitisha(fstat(faili, (void *)0x00100000) == -1 && errno == EFAULT);
    thibitisha(lseek(faili, 0, SEEK_CUR) == 0);
    thibitisha(read(faili, NULL, 0) == 0 && write(faili, NULL, 0) == 0);
    thibitisha(ondoa_faili_ingizo_jina("posix.txt") == 0);
    thibitisha(fstat(faili, &hali_thamani) == 0 && hali_thamani.st_nlink == 0 && hali_thamani.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    thibitisha(새파일 == 5 && fstat(새파일, &hali_thamani) == 0 && hali_thamani.st_size == 0);
    thibitisha(read(faili, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    thibitisha(close(faili) == 0 && close(복제) == 0 && close(새파일) == 0);
    thibitisha(close(새파일) == -1 && errno == EBADF);
    thibitisha(unlink("posix.txt") == 0);
    faili = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    thibitisha(faili == 3 && fcntl(faili, F_GETFD) == 1);
    thibitisha(read(faili, data, 1) == -1 && errno == EBADF);
    thibitisha(write(faili, "keep", 4) == 4);
    for (int kielezo = 4; kielezo < 32; kielezo++) thibitisha(dup(faili) == kielezo);
    thibitisha(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    thibitisha(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    thibitisha(fstat(faili, &hali_thamani) == 0 && hali_thamani.st_size == 4);
    for (int kielezo = 3; kielezo < 32; kielezo++) thibitisha(close(kielezo) == 0);
    thibitisha(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    faili = open("posix.txt", O_RDONLY);
    thibitisha(faili == 3 && write(faili, data, 1) == -1 && errno == EBADF);
    thibitisha(fcntl(faili, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    thibitisha(close(8) == 0 && close(faili) == 0 && unlink("posix.txt") == 0);
    thibitisha(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    thibitisha(fstat(1, &hali_thamani) == 0 && S_ISCHR(hali_thamani.st_mode));
    thibitisha(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    thibitisha(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr anwani; char anwani_SMS[16];
    thibitisha(inet_pton(AF_INET, "10.0.2.2", &anwani) == 1 && ntohl(anwani.s_addr) == 0x0a000202U);
    thibitisha(inet_ntop(AF_INET, &anwani, anwani_SMS, sizeof anwani_SMS) == anwani_SMS && strcmp(anwani_SMS, "10.0.2.2") == 0);
    thibitisha(inet_pton(AF_INET, "256.0.0.1", &anwani) == 0 && ntohl(anwani.s_addr) == 0x0a000202U);
    thibitisha(inet_pton(AF_INET, "01.0.0.1", &anwani) == 0);
    thibitisha(inet_ntop(AF_INET, &anwani, anwani_SMS, 3) == NULL && errno == ENOSPC);
    thibitisha(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Jina[] = "slot0";
    for (int kielezo = 0; kielezo < 8; kielezo++) {
        Jina[4] = '0' + kielezo;
        int 열린파일 = open(Jina, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { thibitisha(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    thibitisha(개수 > 0 && 개수 < 8);
    thibitisha(unlink("slot0") == 0);
    thibitisha(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    thibitisha(close(보관[0]) == 0);
    faili = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    thibitisha(faili >= 0 && close(faili) == 0 && unlink("held-slot") == 0);
    for (int kielezo = 1; kielezo < 개수; kielezo++) {
        Jina[4] = '0' + kielezo;
        thibitisha(close(보관[kielezo]) == 0 && unlink(Jina) == 0);
    }
    thibitisha(fsync(-1) == -1 && errno == EBADF);
    thibitisha(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
