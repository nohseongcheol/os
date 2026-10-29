#include <檔案ABI.h>
#include <網路ABI.h>
#include <string.h>
#include <stdio.h>

static int 已檢查項目個數;
static void 檢查項(int 條件, int 行) {
    已檢查項目個數++;
    if (!條件) {
        puts("POSIX CHECK FAILED");
        char 數字值[12]; int 長度 = 0;
        do { 數字值[長度++] = '0' + 行 % 10; 行 /= 10; } while (行);
        while (長度) putchar(數字值[--長度]);
        putchar('\n'); _exit(1);
    }
}
#define 驗證(條件) 檢查項((條件), __LINE__)

int main(int 參數列個數, char **實際參數列表) {
    char 資料[32]; struct stat 狀態值;
    驗證(參數列個數 == 2 && strcmp(實際參數列表[1], "check") == 0 && 實際參數列表[2] == 0);
    驗證(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    驗證(打開檔案("absent", 讀取僅用值) == -1 && 錯誤編號 == ENOENT);
    int 檔案 = 打開檔案("/posix.txt", 讀取寫入 | 創建新建檔案, 0640);
    驗證(檔案 == 3);
    驗證(寫入檔案資料(檔案, "abcd", 4) == 4);
    驗證(打開檔案("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    驗證(讀取檔案運行狀態(檔案, &狀態值) == 0 && 狀態值.st_size == 4 && S_ISREG(狀態值.st_mode));
    驗證((狀態值.st_mode & 0777) == 0640 && 狀態值.st_nlink == 1);
    驗證(尋道檔案(檔案, 0, 起點開頭) == 0);
    int 克隆值 = 複製副本檔案描述符(檔案);
    驗證(克隆值 == 4);
    驗證(讀取檔案資料(克隆值, 資料, 2) == 2 && memcmp(資料, "ab", 2) == 0);
    驗證(讀取檔案資料(檔案, 資料, 2) == 2 && memcmp(資料, "cd", 2) == 0);
    驗證(讀取檔案資料(檔案, 資料, 1) == 0);
    驗證(fcntl(檔案, F_SETFD, FD_CLOEXEC) == 0 && fcntl(檔案, F_GETFD) == 1);
    驗證(fcntl(克隆值, F_GETFD) == 0);
    驗證(dup2(檔案, 檔案) == 檔案 && fcntl(檔案, F_GETFD) == 1);
    驗證(dup2(-1, 克隆值) == -1 && errno == EBADF && fcntl(克隆值, F_GETFD) == 0);
    驗證(fcntl(克隆值, F_SETFL, O_APPEND) == 0 && (fcntl(檔案, F_GETFL) & O_APPEND));
    驗證(lseek(檔案, 0, SEEK_SET) == 0 && write(克隆值, "e", 1) == 1 && lseek(檔案, 0, SEEK_CUR) == 5);
    驗證(fcntl(檔案, F_SETFL, 0) == 0);
    驗證(lseek(檔案, 8, SEEK_SET) == 8 && write(檔案, "Z", 1) == 1);
    驗證(lseek(克隆值, 5, SEEK_SET) == 5 && read(檔案, 資料, 4) == 4);
    驗證(資料[0] == 0 && 資料[1] == 0 && 資料[2] == 0 && 資料[3] == 'Z');
    驗證(ftruncate(檔案, 2) == 0 && lseek(檔案, 0, SEEK_CUR) == 9);
    驗證(ftruncate(檔案, 6) == 0 && lseek(檔案, 2, SEEK_SET) == 2 && read(檔案, 資料, 4) == 4);
    驗證(!資料[0] && !資料[1] && !資料[2] && !資料[3]);
    驗證(lseek(檔案, 2147483647, SEEK_SET) == 2147483647);
    驗證(lseek(檔案, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    驗證(lseek(檔案, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    驗證(write(檔案, "!", 1) == -1 && errno == EFBIG);
    驗證(lseek(檔案, 0, SEEK_SET) == 0);
    驗證(read(檔案, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    驗證(read(檔案, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    驗證(write(檔案, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    驗證(read(檔案, 資料, (size_t)-1) == -1 && errno == EINVAL);
    驗證(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    驗證(fstat(檔案, (void *)0x00100000) == -1 && errno == EFAULT);
    驗證(lseek(檔案, 0, SEEK_CUR) == 0);
    驗證(read(檔案, NULL, 0) == 0 && write(檔案, NULL, 0) == 0);
    驗證(移除檔案條目名稱("posix.txt") == 0);
    驗證(fstat(檔案, &狀態值) == 0 && 狀態值.st_nlink == 0 && 狀態值.st_size == 6);
    int 新建檔案 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    驗證(新建檔案 == 5 && fstat(新建檔案, &狀態值) == 0 && 狀態值.st_size == 0);
    驗證(read(檔案, 資料, 2) == 2 && memcmp(資料, "ab", 2) == 0);
    驗證(close(檔案) == 0 && close(克隆值) == 0 && close(新建檔案) == 0);
    驗證(close(新建檔案) == -1 && errno == EBADF);
    驗證(unlink("posix.txt") == 0);
    檔案 = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    驗證(檔案 == 3 && fcntl(檔案, F_GETFD) == 1);
    驗證(read(檔案, 資料, 1) == -1 && errno == EBADF);
    驗證(write(檔案, "keep", 4) == 4);
    for (int 編號 = 4; 編號 < 32; 編號++) 驗證(dup(檔案) == 編號);
    驗證(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    驗證(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    驗證(fstat(檔案, &狀態值) == 0 && 狀態值.st_size == 4);
    for (int 編號 = 3; 編號 < 32; 編號++) 驗證(close(編號) == 0);
    驗證(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    檔案 = open("posix.txt", O_RDONLY);
    驗證(檔案 == 3 && write(檔案, 資料, 1) == -1 && errno == EBADF);
    驗證(fcntl(檔案, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    驗證(close(8) == 0 && close(檔案) == 0 && unlink("posix.txt") == 0);
    驗證(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    驗證(fstat(1, &狀態值) == 0 && S_ISCHR(狀態值.st_mode));
    驗證(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    驗證(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr 地址; char 地址文本[16];
    驗證(inet_pton(AF_INET, "10.0.2.2", &地址) == 1 && ntohl(地址.s_addr) == 0x0a000202U);
    驗證(inet_ntop(AF_INET, &地址, 地址文本, sizeof 地址文本) == 地址文本 && strcmp(地址文本, "10.0.2.2") == 0);
    驗證(inet_pton(AF_INET, "256.0.0.1", &地址) == 0 && ntohl(地址.s_addr) == 0x0a000202U);
    驗證(inet_pton(AF_INET, "01.0.0.1", &地址) == 0);
    驗證(inet_ntop(AF_INET, &地址, 地址文本, 3) == NULL && errno == ENOSPC);
    驗證(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 保留值[8], 項目個數 = 0; char 名稱[] = "slot0";
    for (int 編號 = 0; 編號 < 8; 編號++) {
        名稱[4] = '0' + 編號;
        int 已打開檔案 = open(名稱, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (已打開檔案 < 0) { 驗證(errno == ENOSPC); break; }
        保留值[項目個數++] = 已打開檔案;
    }
    驗證(項目個數 > 0 && 項目個數 < 8);
    驗證(unlink("slot0") == 0);
    驗證(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    驗證(close(保留值[0]) == 0);
    檔案 = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    驗證(檔案 >= 0 && close(檔案) == 0 && unlink("held-slot") == 0);
    for (int 編號 = 1; 編號 < 項目個數; 編號++) {
        名稱[4] = '0' + 編號;
        驗證(close(保留值[編號]) == 0 && unlink(名稱) == 0);
    }
    驗證(fsync(-1) == -1 && errno == EBADF);
    驗證(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
