#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int here, int hononga) {
    검사항목수++;
    if (!here) {
        puts("POSIX CHECK FAILED");
        char mati_uara[12]; int roa_uara = 0;
        do { mati_uara[roa_uara++] = '0' + hononga % 10; hononga /= 10; } while (hononga);
        while (roa_uara) putchar(mati_uara[--roa_uara]);
        putchar('\n'); _exit(1);
    }
}
#define manatoko(here) 검사((here), __LINE__)

int main(int 인수개수, char **tohenga_Rārangi) {
    char raraunga[32]; struct stat tūnga_uara;
    manatoko(인수개수 == 2 && strcmp(tohenga_Rārangi[1], "check") == 0 && tohenga_Rārangi[2] == 0);
    manatoko(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    manatoko(tiwhikete_kōnae("absent", pānui_anake_uara) == -1 && 오류번호 == ENOENT);
    int Kōnae = tiwhikete_kōnae("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    manatoko(Kōnae == 3);
    manatoko(tuhi_kōnae_raraunga(Kōnae, "abcd", 4) == 4);
    manatoko(tiwhikete_kōnae("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    manatoko(파일상태읽기(Kōnae, &tūnga_uara) == 0 && tūnga_uara.st_size == 4 && S_ISREG(tūnga_uara.st_mode));
    manatoko((tūnga_uara.st_mode & 0777) == 0640 && tūnga_uara.st_nlink == 1);
    manatoko(kimi_kōnae(Kōnae, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Kōnae);
    manatoko(복제 == 4);
    manatoko(파일자료읽기(복제, raraunga, 2) == 2 && memcmp(raraunga, "ab", 2) == 0);
    manatoko(파일자료읽기(Kōnae, raraunga, 2) == 2 && memcmp(raraunga, "cd", 2) == 0);
    manatoko(파일자료읽기(Kōnae, raraunga, 1) == 0);
    manatoko(fcntl(Kōnae, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Kōnae, F_GETFD) == 1);
    manatoko(fcntl(복제, F_GETFD) == 0);
    manatoko(dup2(Kōnae, Kōnae) == Kōnae && fcntl(Kōnae, F_GETFD) == 1);
    manatoko(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    manatoko(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Kōnae, F_GETFL) & O_APPEND));
    manatoko(lseek(Kōnae, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Kōnae, 0, SEEK_CUR) == 5);
    manatoko(fcntl(Kōnae, F_SETFL, 0) == 0);
    manatoko(lseek(Kōnae, 8, SEEK_SET) == 8 && write(Kōnae, "Z", 1) == 1);
    manatoko(lseek(복제, 5, SEEK_SET) == 5 && read(Kōnae, raraunga, 4) == 4);
    manatoko(raraunga[0] == 0 && raraunga[1] == 0 && raraunga[2] == 0 && raraunga[3] == 'Z');
    manatoko(ftruncate(Kōnae, 2) == 0 && lseek(Kōnae, 0, SEEK_CUR) == 9);
    manatoko(ftruncate(Kōnae, 6) == 0 && lseek(Kōnae, 2, SEEK_SET) == 2 && read(Kōnae, raraunga, 4) == 4);
    manatoko(!raraunga[0] && !raraunga[1] && !raraunga[2] && !raraunga[3]);
    manatoko(lseek(Kōnae, 2147483647, SEEK_SET) == 2147483647);
    manatoko(lseek(Kōnae, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    manatoko(lseek(Kōnae, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    manatoko(write(Kōnae, "!", 1) == -1 && errno == EFBIG);
    manatoko(lseek(Kōnae, 0, SEEK_SET) == 0);
    manatoko(read(Kōnae, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    manatoko(read(Kōnae, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    manatoko(write(Kōnae, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    manatoko(read(Kōnae, raraunga, (size_t)-1) == -1 && errno == EINVAL);
    manatoko(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    manatoko(fstat(Kōnae, (void *)0x00100000) == -1 && errno == EFAULT);
    manatoko(lseek(Kōnae, 0, SEEK_CUR) == 0);
    manatoko(read(Kōnae, NULL, 0) == 0 && write(Kōnae, NULL, 0) == 0);
    manatoko(tango_kōnae_tāurunga_ingoa("posix.txt") == 0);
    manatoko(fstat(Kōnae, &tūnga_uara) == 0 && tūnga_uara.st_nlink == 0 && tūnga_uara.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    manatoko(새파일 == 5 && fstat(새파일, &tūnga_uara) == 0 && tūnga_uara.st_size == 0);
    manatoko(read(Kōnae, raraunga, 2) == 2 && memcmp(raraunga, "ab", 2) == 0);
    manatoko(close(Kōnae) == 0 && close(복제) == 0 && close(새파일) == 0);
    manatoko(close(새파일) == -1 && errno == EBADF);
    manatoko(unlink("posix.txt") == 0);
    Kōnae = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    manatoko(Kōnae == 3 && fcntl(Kōnae, F_GETFD) == 1);
    manatoko(read(Kōnae, raraunga, 1) == -1 && errno == EBADF);
    manatoko(write(Kōnae, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) manatoko(dup(Kōnae) == INDEX);
    manatoko(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    manatoko(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    manatoko(fstat(Kōnae, &tūnga_uara) == 0 && tūnga_uara.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) manatoko(close(INDEX) == 0);
    manatoko(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Kōnae = open("posix.txt", O_RDONLY);
    manatoko(Kōnae == 3 && write(Kōnae, raraunga, 1) == -1 && errno == EBADF);
    manatoko(fcntl(Kōnae, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    manatoko(close(8) == 0 && close(Kōnae) == 0 && unlink("posix.txt") == 0);
    manatoko(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    manatoko(fstat(1, &tūnga_uara) == 0 && S_ISCHR(tūnga_uara.st_mode));
    manatoko(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    manatoko(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_TEXT[16];
    manatoko(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    manatoko(inet_ntop(AF_INET, &ADDRESS, ADDRESS_TEXT, sizeof ADDRESS_TEXT) == ADDRESS_TEXT && strcmp(ADDRESS_TEXT, "10.0.2.2") == 0);
    manatoko(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    manatoko(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    manatoko(inet_ntop(AF_INET, &ADDRESS, ADDRESS_TEXT, 3) == NULL && errno == ENOSPC);
    manatoko(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], tuemi_COUNT = 0; char Ingoa[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Ingoa[4] = '0' + INDEX;
        int 열린파일 = open(Ingoa, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { manatoko(errno == ENOSPC); break; }
        보관[tuemi_COUNT++] = 열린파일;
    }
    manatoko(tuemi_COUNT > 0 && tuemi_COUNT < 8);
    manatoko(unlink("slot0") == 0);
    manatoko(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    manatoko(close(보관[0]) == 0);
    Kōnae = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    manatoko(Kōnae >= 0 && close(Kōnae) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < tuemi_COUNT; INDEX++) {
        Ingoa[4] = '0' + INDEX;
        manatoko(close(보관[INDEX]) == 0 && unlink(Ingoa) == 0);
    }
    manatoko(fsync(-1) == -1 && errno == EBADF);
    manatoko(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
