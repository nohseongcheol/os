#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int నిబంధన, int పంక్తి) {
    검사항목수++;
    if (!నిబంధన) {
        puts("POSIX CHECK FAILED");
        char అంకె_మూల్యం[12]; int పొడవు_మూల్యం = 0;
        do { అంకె_మూల్యం[పొడవు_మూల్యం++] = '0' + పంక్తి % 10; పంక్తి /= 10; } while (పంక్తి);
        while (పొడవు_మూల్యం) putchar(అంకె_మూల్యం[--పొడవు_మూల్యం]);
        putchar('\n'); _exit(1);
    }
}
#define సరిచూడు(నిబంధన) 검사((నిబంధన), __LINE__)

int main(int 인수개수, char **కారకం_జాబితా) {
    char డేటా[32]; struct stat స్థితి_మూల్యం;
    సరిచూడు(인수개수 == 2 && strcmp(కారకం_జాబితా[1], "check") == 0 && కారకం_జాబితా[2] == 0);
    సరిచూడు(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    సరిచూడు(తెరువు_ఫైలు("absent", చదవడానికి_మాత్రమే_మూల్యం) == -1 && 오류번호 == ENOENT);
    int దస్త్రం = తెరువు_ఫైలు("/posix.txt", పఠన_లేఖన | 새파일만들기, 0640);
    సరిచూడు(దస్త్రం == 3);
    సరిచూడు(వ్రాయి_ఫైలు_డేటా(దస్త్రం, "abcd", 4) == 4);
    సరిచూడు(తెరువు_ఫైలు("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    సరిచూడు(파일상태읽기(దస్త్రం, &స్థితి_మూల్యం) == 0 && స్థితి_మూల్యం.st_size == 4 && S_ISREG(స్థితి_మూల్యం.st_mode));
    సరిచూడు((స్థితి_మూల్యం.st_mode & 0777) == 0640 && స్థితి_మూల్యం.st_nlink == 1);
    సరిచూడు(శోధించు_ఫైలు(దస్త్రం, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(దస్త్రం);
    సరిచూడు(복제 == 4);
    సరిచూడు(파일자료읽기(복제, డేటా, 2) == 2 && memcmp(డేటా, "ab", 2) == 0);
    సరిచూడు(파일자료읽기(దస్త్రం, డేటా, 2) == 2 && memcmp(డేటా, "cd", 2) == 0);
    సరిచూడు(파일자료읽기(దస్త్రం, డేటా, 1) == 0);
    సరిచూడు(fcntl(దస్త్రం, F_SETFD, FD_CLOEXEC) == 0 && fcntl(దస్త్రం, F_GETFD) == 1);
    సరిచూడు(fcntl(복제, F_GETFD) == 0);
    సరిచూడు(dup2(దస్త్రం, దస్త్రం) == దస్త్రం && fcntl(దస్త్రం, F_GETFD) == 1);
    సరిచూడు(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    సరిచూడు(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(దస్త్రం, F_GETFL) & O_APPEND));
    సరిచూడు(lseek(దస్త్రం, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(దస్త్రం, 0, SEEK_CUR) == 5);
    సరిచూడు(fcntl(దస్త్రం, F_SETFL, 0) == 0);
    సరిచూడు(lseek(దస్త్రం, 8, SEEK_SET) == 8 && write(దస్త్రం, "Z", 1) == 1);
    సరిచూడు(lseek(복제, 5, SEEK_SET) == 5 && read(దస్త్రం, డేటా, 4) == 4);
    సరిచూడు(డేటా[0] == 0 && డేటా[1] == 0 && డేటా[2] == 0 && డేటా[3] == 'Z');
    సరిచూడు(ftruncate(దస్త్రం, 2) == 0 && lseek(దస్త్రం, 0, SEEK_CUR) == 9);
    సరిచూడు(ftruncate(దస్త్రం, 6) == 0 && lseek(దస్త్రం, 2, SEEK_SET) == 2 && read(దస్త్రం, డేటా, 4) == 4);
    సరిచూడు(!డేటా[0] && !డేటా[1] && !డేటా[2] && !డేటా[3]);
    సరిచూడు(lseek(దస్త్రం, 2147483647, SEEK_SET) == 2147483647);
    సరిచూడు(lseek(దస్త్రం, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    సరిచూడు(lseek(దస్త్రం, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    సరిచూడు(write(దస్త్రం, "!", 1) == -1 && errno == EFBIG);
    సరిచూడు(lseek(దస్త్రం, 0, SEEK_SET) == 0);
    సరిచూడు(read(దస్త్రం, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    సరిచూడు(read(దస్త్రం, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    సరిచూడు(write(దస్త్రం, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    సరిచూడు(read(దస్త్రం, డేటా, (size_t)-1) == -1 && errno == EINVAL);
    సరిచూడు(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    సరిచూడు(fstat(దస్త్రం, (void *)0x00100000) == -1 && errno == EFAULT);
    సరిచూడు(lseek(దస్త్రం, 0, SEEK_CUR) == 0);
    సరిచూడు(read(దస్త్రం, NULL, 0) == 0 && write(దస్త్రం, NULL, 0) == 0);
    సరిచూడు(తీసివెయ్యి_ఫైలు_ప్రవేశం_పేరు("posix.txt") == 0);
    సరిచూడు(fstat(దస్త్రం, &స్థితి_మూల్యం) == 0 && స్థితి_మూల్యం.st_nlink == 0 && స్థితి_మూల్యం.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    సరిచూడు(새파일 == 5 && fstat(새파일, &స్థితి_మూల్యం) == 0 && స్థితి_మూల్యం.st_size == 0);
    సరిచూడు(read(దస్త్రం, డేటా, 2) == 2 && memcmp(డేటా, "ab", 2) == 0);
    సరిచూడు(close(దస్త్రం) == 0 && close(복제) == 0 && close(새파일) == 0);
    సరిచూడు(close(새파일) == -1 && errno == EBADF);
    సరిచూడు(unlink("posix.txt") == 0);
    దస్త్రం = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    సరిచూడు(దస్త్రం == 3 && fcntl(దస్త్రం, F_GETFD) == 1);
    సరిచూడు(read(దస్త్రం, డేటా, 1) == -1 && errno == EBADF);
    సరిచూడు(write(దస్త్రం, "keep", 4) == 4);
    for (int సూచీ = 4; సూచీ < 32; సూచీ++) సరిచూడు(dup(దస్త్రం) == సూచీ);
    సరిచూడు(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    సరిచూడు(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    సరిచూడు(fstat(దస్త్రం, &స్థితి_మూల్యం) == 0 && స్థితి_మూల్యం.st_size == 4);
    for (int సూచీ = 3; సూచీ < 32; సూచీ++) సరిచూడు(close(సూచీ) == 0);
    సరిచూడు(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    దస్త్రం = open("posix.txt", O_RDONLY);
    సరిచూడు(దస్త్రం == 3 && write(దస్త్రం, డేటా, 1) == -1 && errno == EBADF);
    సరిచూడు(fcntl(దస్త్రం, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    సరిచూడు(close(8) == 0 && close(దస్త్రం) == 0 && unlink("posix.txt") == 0);
    సరిచూడు(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    సరిచూడు(fstat(1, &స్థితి_మూల్యం) == 0 && S_ISCHR(స్థితి_మూల్యం.st_mode));
    సరిచూడు(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    సరిచూడు(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ఇమెయిల్; char ఇమెయిల్_పాఠం[16];
    సరిచూడు(inet_pton(AF_INET, "10.0.2.2", &ఇమెయిల్) == 1 && ntohl(ఇమెయిల్.s_addr) == 0x0a000202U);
    సరిచూడు(inet_ntop(AF_INET, &ఇమెయిల్, ఇమెయిల్_పాఠం, sizeof ఇమెయిల్_పాఠం) == ఇమెయిల్_పాఠం && strcmp(ఇమెయిల్_పాఠం, "10.0.2.2") == 0);
    సరిచూడు(inet_pton(AF_INET, "256.0.0.1", &ఇమెయిల్) == 0 && ntohl(ఇమెయిల్.s_addr) == 0x0a000202U);
    సరిచూడు(inet_pton(AF_INET, "01.0.0.1", &ఇమెయిల్) == 0);
    సరిచూడు(inet_ntop(AF_INET, &ఇమెయిల్, ఇమెయిల్_పాఠం, 3) == NULL && errno == ENOSPC);
    సరిచూడు(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char పేరు[] = "slot0";
    for (int సూచీ = 0; సూచీ < 8; సూచీ++) {
        పేరు[4] = '0' + సూచీ;
        int 열린파일 = open(పేరు, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { సరిచూడు(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    సరిచూడు(개수 > 0 && 개수 < 8);
    సరిచూడు(unlink("slot0") == 0);
    సరిచూడు(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    సరిచూడు(close(보관[0]) == 0);
    దస్త్రం = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    సరిచూడు(దస్త్రం >= 0 && close(దస్త్రం) == 0 && unlink("held-slot") == 0);
    for (int సూచీ = 1; సూచీ < 개수; సూచీ++) {
        పేరు[4] = '0' + సూచీ;
        సరిచూడు(close(보관[సూచీ]) == 0 && unlink(పేరు) == 0);
    }
    సరిచూడు(fsync(-1) == -1 && errno == EBADF);
    సరిచూడు(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
