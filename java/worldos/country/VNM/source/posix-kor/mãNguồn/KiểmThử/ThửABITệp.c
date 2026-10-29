#include <ABITệp.h>
#include <ABIMạng.h>
#include <string.h>
#include <stdio.h>

static int sốLượngPhầnMụcĐãKiểmTra;
static void CácPhépKiểmTra(int điềuKiện, int dòng) {
    sốLượngPhầnMụcĐãKiểmTra++;
    if (!điềuKiện) {
        puts("POSIX CHECK FAILED");
        char giáTrịChữSố[12]; int độDài = 0;
        do { giáTrịChữSố[độDài++] = '0' + dòng % 10; dòng /= 10; } while (dòng);
        while (độDài) putchar(giáTrịChữSố[--độDài]);
        putchar('\n'); _exit(1);
    }
}
#define xácMinh(điềuKiện) CácPhépKiểmTra((điềuKiện), __LINE__)

int main(int sốLượngCácĐốiSố, char **danhSáchĐốiSố) {
    char DữLiệu[32]; struct stat giáTrịTrạngThái;
    xácMinh(sốLượngCácĐốiSố == 2 && strcmp(danhSáchĐốiSố[1], "check") == 0 && danhSáchĐốiSố[2] == 0);
    xácMinh(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    xácMinh(mởTệp("absent", đọcGiáTrịChỉ) == -1 && sốLỗi == ENOENT);
    int Tệp = mởTệp("/posix.txt", GhiĐọc | tạoTệpMới, 0640);
    xácMinh(Tệp == 3);
    xácMinh(ghiDữLiệuTệp(Tệp, "abcd", 4) == 4);
    xácMinh(mởTệp("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    xácMinh(đọcTìnhTrạngTệp(Tệp, &giáTrịTrạngThái) == 0 && giáTrịTrạngThái.st_size == 4 && S_ISREG(giáTrịTrạngThái.st_mode));
    xácMinh((giáTrịTrạngThái.st_mode & 0777) == 0640 && giáTrịTrạngThái.st_nlink == 1);
    xácMinh(dịchVịTệp(Tệp, 0, PhầnĐầuTừ) == 0);
    int giáTrịNhânBản = bộMôTảTệpBảnSao(Tệp);
    xácMinh(giáTrịNhânBản == 4);
    xácMinh(đọcDữLiệuTệp(giáTrịNhânBản, DữLiệu, 2) == 2 && memcmp(DữLiệu, "ab", 2) == 0);
    xácMinh(đọcDữLiệuTệp(Tệp, DữLiệu, 2) == 2 && memcmp(DữLiệu, "cd", 2) == 0);
    xácMinh(đọcDữLiệuTệp(Tệp, DữLiệu, 1) == 0);
    xácMinh(fcntl(Tệp, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Tệp, F_GETFD) == 1);
    xácMinh(fcntl(giáTrịNhânBản, F_GETFD) == 0);
    xácMinh(dup2(Tệp, Tệp) == Tệp && fcntl(Tệp, F_GETFD) == 1);
    xácMinh(dup2(-1, giáTrịNhânBản) == -1 && errno == EBADF && fcntl(giáTrịNhânBản, F_GETFD) == 0);
    xácMinh(fcntl(giáTrịNhânBản, F_SETFL, O_APPEND) == 0 && (fcntl(Tệp, F_GETFL) & O_APPEND));
    xácMinh(lseek(Tệp, 0, SEEK_SET) == 0 && write(giáTrịNhânBản, "e", 1) == 1 && lseek(Tệp, 0, SEEK_CUR) == 5);
    xácMinh(fcntl(Tệp, F_SETFL, 0) == 0);
    xácMinh(lseek(Tệp, 8, SEEK_SET) == 8 && write(Tệp, "Z", 1) == 1);
    xácMinh(lseek(giáTrịNhânBản, 5, SEEK_SET) == 5 && read(Tệp, DữLiệu, 4) == 4);
    xácMinh(DữLiệu[0] == 0 && DữLiệu[1] == 0 && DữLiệu[2] == 0 && DữLiệu[3] == 'Z');
    xácMinh(ftruncate(Tệp, 2) == 0 && lseek(Tệp, 0, SEEK_CUR) == 9);
    xácMinh(ftruncate(Tệp, 6) == 0 && lseek(Tệp, 2, SEEK_SET) == 2 && read(Tệp, DữLiệu, 4) == 4);
    xácMinh(!DữLiệu[0] && !DữLiệu[1] && !DữLiệu[2] && !DữLiệu[3]);
    xácMinh(lseek(Tệp, 2147483647, SEEK_SET) == 2147483647);
    xácMinh(lseek(Tệp, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    xácMinh(lseek(Tệp, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    xácMinh(write(Tệp, "!", 1) == -1 && errno == EFBIG);
    xácMinh(lseek(Tệp, 0, SEEK_SET) == 0);
    xácMinh(read(Tệp, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    xácMinh(read(Tệp, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    xácMinh(write(Tệp, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    xácMinh(read(Tệp, DữLiệu, (size_t)-1) == -1 && errno == EINVAL);
    xácMinh(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    xácMinh(fstat(Tệp, (void *)0x00100000) == -1 && errno == EFAULT);
    xácMinh(lseek(Tệp, 0, SEEK_CUR) == 0);
    xácMinh(read(Tệp, NULL, 0) == 0 && write(Tệp, NULL, 0) == 0);
    xácMinh(gỡTênMụcTệp("posix.txt") == 0);
    xácMinh(fstat(Tệp, &giáTrịTrạngThái) == 0 && giáTrịTrạngThái.st_nlink == 0 && giáTrịTrạngThái.st_size == 6);
    int tệpMới = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    xácMinh(tệpMới == 5 && fstat(tệpMới, &giáTrịTrạngThái) == 0 && giáTrịTrạngThái.st_size == 0);
    xácMinh(read(Tệp, DữLiệu, 2) == 2 && memcmp(DữLiệu, "ab", 2) == 0);
    xácMinh(close(Tệp) == 0 && close(giáTrịNhânBản) == 0 && close(tệpMới) == 0);
    xácMinh(close(tệpMới) == -1 && errno == EBADF);
    xácMinh(unlink("posix.txt") == 0);
    Tệp = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    xácMinh(Tệp == 3 && fcntl(Tệp, F_GETFD) == 1);
    xácMinh(read(Tệp, DữLiệu, 1) == -1 && errno == EBADF);
    xácMinh(write(Tệp, "keep", 4) == 4);
    for (int sốHiệu = 4; sốHiệu < 32; sốHiệu++) xácMinh(dup(Tệp) == sốHiệu);
    xácMinh(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    xácMinh(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    xácMinh(fstat(Tệp, &giáTrịTrạngThái) == 0 && giáTrịTrạngThái.st_size == 4);
    for (int sốHiệu = 3; sốHiệu < 32; sốHiệu++) xácMinh(close(sốHiệu) == 0);
    xácMinh(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Tệp = open("posix.txt", O_RDONLY);
    xácMinh(Tệp == 3 && write(Tệp, DữLiệu, 1) == -1 && errno == EBADF);
    xácMinh(fcntl(Tệp, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    xácMinh(close(8) == 0 && close(Tệp) == 0 && unlink("posix.txt") == 0);
    xácMinh(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    xácMinh(fstat(1, &giáTrịTrạngThái) == 0 && S_ISCHR(giáTrịTrạngThái.st_mode));
    xácMinh(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    xácMinh(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr địaChỉ; char vănBảnĐịaChỉ[16];
    xácMinh(inet_pton(AF_INET, "10.0.2.2", &địaChỉ) == 1 && ntohl(địaChỉ.s_addr) == 0x0a000202U);
    xácMinh(inet_ntop(AF_INET, &địaChỉ, vănBảnĐịaChỉ, sizeof vănBảnĐịaChỉ) == vănBảnĐịaChỉ && strcmp(vănBảnĐịaChỉ, "10.0.2.2") == 0);
    xácMinh(inet_pton(AF_INET, "256.0.0.1", &địaChỉ) == 0 && ntohl(địaChỉ.s_addr) == 0x0a000202U);
    xácMinh(inet_pton(AF_INET, "01.0.0.1", &địaChỉ) == 0);
    xácMinh(inet_ntop(AF_INET, &địaChỉ, vănBảnĐịaChỉ, 3) == NULL && errno == ENOSPC);
    xácMinh(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int giữNguyênGiáTrị[8], sốLượngPhầnMục = 0; char tên[] = "slot0";
    for (int sốHiệu = 0; sốHiệu < 8; sốHiệu++) {
        tên[4] = '0' + sốHiệu;
        int tệpĐãMở = open(tên, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (tệpĐãMở < 0) { xácMinh(errno == ENOSPC); break; }
        giữNguyênGiáTrị[sốLượngPhầnMục++] = tệpĐãMở;
    }
    xácMinh(sốLượngPhầnMục > 0 && sốLượngPhầnMục < 8);
    xácMinh(unlink("slot0") == 0);
    xácMinh(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    xácMinh(close(giữNguyênGiáTrị[0]) == 0);
    Tệp = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    xácMinh(Tệp >= 0 && close(Tệp) == 0 && unlink("held-slot") == 0);
    for (int sốHiệu = 1; sốHiệu < sốLượngPhầnMục; sốHiệu++) {
        tên[4] = '0' + sốHiệu;
        xácMinh(close(giữNguyênGiáTrị[sốHiệu]) == 0 && unlink(tên) == 0);
    }
    xácMinh(fsync(-1) == -1 && errno == EBADF);
    xácMinh(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
