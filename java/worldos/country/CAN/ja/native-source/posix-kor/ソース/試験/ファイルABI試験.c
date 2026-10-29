#include <ファイルABI.h>
#include <通信網ABI.h>
#include <string.h>
#include <stdio.h>

static int 検査済み項目個数;
static void 検査項目(int 条件, int 行) {
    検査済み項目個数++;
    if (!条件) {
        puts("POSIX CHECK FAILED");
        char 桁値[12]; int 長さ = 0;
        do { 桁値[長さ++] = '0' + 行 % 10; 行 /= 10; } while (行);
        while (長さ) putchar(桁値[--長さ]);
        putchar('\n'); _exit(1);
    }
}
#define 検証(条件) 検査項目((条件), __LINE__)

int main(int 引数列個数, char **引数一覧) {
    char データ[32]; struct stat 状況値;
    検証(引数列個数 == 2 && strcmp(引数一覧[1], "check") == 0 && 引数一覧[2] == 0);
    検証(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    検証(ファイル開放("absent", 専用値読取) == -1 && エラー番号 == ENOENT);
    int ファイル = ファイル開放("/posix.txt", 読取書込 | 新規ファイル作成, 0640);
    検証(ファイル == 3);
    検証(ファイルデータ書込(ファイル, "abcd", 4) == 4);
    検証(ファイル開放("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    検証(ファイル状態読取(ファイル, &状況値) == 0 && 状況値.st_size == 4 && S_ISREG(状況値.st_mode));
    検証((状況値.st_mode & 0777) == 0640 && 状況値.st_nlink == 1);
    検証(ファイル位置移動(ファイル, 0, 起点先頭) == 0);
    int 複製処理値 = 複製ファイル記述子(ファイル);
    検証(複製処理値 == 4);
    検証(ファイルデータ読取(複製処理値, データ, 2) == 2 && memcmp(データ, "ab", 2) == 0);
    検証(ファイルデータ読取(ファイル, データ, 2) == 2 && memcmp(データ, "cd", 2) == 0);
    検証(ファイルデータ読取(ファイル, データ, 1) == 0);
    検証(fcntl(ファイル, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ファイル, F_GETFD) == 1);
    検証(fcntl(複製処理値, F_GETFD) == 0);
    検証(dup2(ファイル, ファイル) == ファイル && fcntl(ファイル, F_GETFD) == 1);
    検証(dup2(-1, 複製処理値) == -1 && errno == EBADF && fcntl(複製処理値, F_GETFD) == 0);
    検証(fcntl(複製処理値, F_SETFL, O_APPEND) == 0 && (fcntl(ファイル, F_GETFL) & O_APPEND));
    検証(lseek(ファイル, 0, SEEK_SET) == 0 && write(複製処理値, "e", 1) == 1 && lseek(ファイル, 0, SEEK_CUR) == 5);
    検証(fcntl(ファイル, F_SETFL, 0) == 0);
    検証(lseek(ファイル, 8, SEEK_SET) == 8 && write(ファイル, "Z", 1) == 1);
    検証(lseek(複製処理値, 5, SEEK_SET) == 5 && read(ファイル, データ, 4) == 4);
    検証(データ[0] == 0 && データ[1] == 0 && データ[2] == 0 && データ[3] == 'Z');
    検証(ftruncate(ファイル, 2) == 0 && lseek(ファイル, 0, SEEK_CUR) == 9);
    検証(ftruncate(ファイル, 6) == 0 && lseek(ファイル, 2, SEEK_SET) == 2 && read(ファイル, データ, 4) == 4);
    検証(!データ[0] && !データ[1] && !データ[2] && !データ[3]);
    検証(lseek(ファイル, 2147483647, SEEK_SET) == 2147483647);
    検証(lseek(ファイル, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    検証(lseek(ファイル, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    検証(write(ファイル, "!", 1) == -1 && errno == EFBIG);
    検証(lseek(ファイル, 0, SEEK_SET) == 0);
    検証(read(ファイル, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    検証(read(ファイル, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    検証(write(ファイル, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    検証(read(ファイル, データ, (size_t)-1) == -1 && errno == EINVAL);
    検証(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    検証(fstat(ファイル, (void *)0x00100000) == -1 && errno == EFAULT);
    検証(lseek(ファイル, 0, SEEK_CUR) == 0);
    検証(read(ファイル, NULL, 0) == 0 && write(ファイル, NULL, 0) == 0);
    検証(ファイル入口名前除去("posix.txt") == 0);
    検証(fstat(ファイル, &状況値) == 0 && 状況値.st_nlink == 0 && 状況値.st_size == 6);
    int 新規ファイル = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    検証(新規ファイル == 5 && fstat(新規ファイル, &状況値) == 0 && 状況値.st_size == 0);
    検証(read(ファイル, データ, 2) == 2 && memcmp(データ, "ab", 2) == 0);
    検証(close(ファイル) == 0 && close(複製処理値) == 0 && close(新規ファイル) == 0);
    検証(close(新規ファイル) == -1 && errno == EBADF);
    検証(unlink("posix.txt") == 0);
    ファイル = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    検証(ファイル == 3 && fcntl(ファイル, F_GETFD) == 1);
    検証(read(ファイル, データ, 1) == -1 && errno == EBADF);
    検証(write(ファイル, "keep", 4) == 4);
    for (int 番号 = 4; 番号 < 32; 番号++) 検証(dup(ファイル) == 番号);
    検証(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    検証(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    検証(fstat(ファイル, &状況値) == 0 && 状況値.st_size == 4);
    for (int 番号 = 3; 番号 < 32; 番号++) 検証(close(番号) == 0);
    検証(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ファイル = open("posix.txt", O_RDONLY);
    検証(ファイル == 3 && write(ファイル, データ, 1) == -1 && errno == EBADF);
    検証(fcntl(ファイル, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    検証(close(8) == 0 && close(ファイル) == 0 && unlink("posix.txt") == 0);
    検証(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    検証(fstat(1, &状況値) == 0 && S_ISCHR(状況値.st_mode));
    検証(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    検証(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr 番地; char 番地本文[16];
    検証(inet_pton(AF_INET, "10.0.2.2", &番地) == 1 && ntohl(番地.s_addr) == 0x0a000202U);
    検証(inet_ntop(AF_INET, &番地, 番地本文, sizeof 番地本文) == 番地本文 && strcmp(番地本文, "10.0.2.2") == 0);
    検証(inet_pton(AF_INET, "256.0.0.1", &番地) == 0 && ntohl(番地.s_addr) == 0x0a000202U);
    検証(inet_pton(AF_INET, "01.0.0.1", &番地) == 0);
    検証(inet_ntop(AF_INET, &番地, 番地本文, 3) == NULL && errno == ENOSPC);
    検証(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 値保持[8], 項目個数 = 0; char 名前[] = "slot0";
    for (int 番号 = 0; 番号 < 8; 番号++) {
        名前[4] = '0' + 番号;
        int 開放済みファイル = open(名前, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (開放済みファイル < 0) { 検証(errno == ENOSPC); break; }
        値保持[項目個数++] = 開放済みファイル;
    }
    検証(項目個数 > 0 && 項目個数 < 8);
    検証(unlink("slot0") == 0);
    検証(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    検証(close(値保持[0]) == 0);
    ファイル = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    検証(ファイル >= 0 && close(ファイル) == 0 && unlink("held-slot") == 0);
    for (int 番号 = 1; 番号 < 項目個数; 番号++) {
        名前[4] = '0' + 番号;
        検証(close(値保持[番号]) == 0 && unlink(名前) == 0);
    }
    検証(fsync(-1) == -1 && errno == EBADF);
    検証(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
