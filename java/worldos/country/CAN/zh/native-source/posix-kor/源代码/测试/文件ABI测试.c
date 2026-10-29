#include <文件ABI.h>
#include <网络ABI.h>
#include <string.h>
#include <stdio.h>

static int 已检查项目个数;
static void 检查项(int 条件, int 行) {
    已检查项目个数++;
    if (!条件) {
        puts("POSIX CHECK FAILED");
        char 数字值[12]; int 长度 = 0;
        do { 数字值[长度++] = '0' + 行 % 10; 行 /= 10; } while (行);
        while (长度) putchar(数字值[--长度]);
        putchar('\n'); _exit(1);
    }
}
#define 验证(条件) 检查项((条件), __LINE__)

int main(int 参数列个数, char **参数列表) {
    char 数据[32]; struct stat 状态值;
    验证(参数列个数 == 2 && strcmp(参数列表[1], "check") == 0 && 参数列表[2] == 0);
    验证(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    验证(打开文件("absent", 读取仅用值) == -1 && 错误编号 == ENOENT);
    int 文件 = 打开文件("/posix.txt", 读取写入 | 创建新建文件, 0640);
    验证(文件 == 3);
    验证(写入文件数据(文件, "abcd", 4) == 4);
    验证(打开文件("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    验证(读取文件运行状态(文件, &状态值) == 0 && 状态值.st_size == 4 && S_ISREG(状态值.st_mode));
    验证((状态值.st_mode & 0777) == 0640 && 状态值.st_nlink == 1);
    验证(寻道文件(文件, 0, 起点开头) == 0);
    int 克隆值 = 复制副本文件描述符(文件);
    验证(克隆值 == 4);
    验证(读取文件数据(克隆值, 数据, 2) == 2 && memcmp(数据, "ab", 2) == 0);
    验证(读取文件数据(文件, 数据, 2) == 2 && memcmp(数据, "cd", 2) == 0);
    验证(读取文件数据(文件, 数据, 1) == 0);
    验证(fcntl(文件, F_SETFD, FD_CLOEXEC) == 0 && fcntl(文件, F_GETFD) == 1);
    验证(fcntl(克隆值, F_GETFD) == 0);
    验证(dup2(文件, 文件) == 文件 && fcntl(文件, F_GETFD) == 1);
    验证(dup2(-1, 克隆值) == -1 && errno == EBADF && fcntl(克隆值, F_GETFD) == 0);
    验证(fcntl(克隆值, F_SETFL, O_APPEND) == 0 && (fcntl(文件, F_GETFL) & O_APPEND));
    验证(lseek(文件, 0, SEEK_SET) == 0 && write(克隆值, "e", 1) == 1 && lseek(文件, 0, SEEK_CUR) == 5);
    验证(fcntl(文件, F_SETFL, 0) == 0);
    验证(lseek(文件, 8, SEEK_SET) == 8 && write(文件, "Z", 1) == 1);
    验证(lseek(克隆值, 5, SEEK_SET) == 5 && read(文件, 数据, 4) == 4);
    验证(数据[0] == 0 && 数据[1] == 0 && 数据[2] == 0 && 数据[3] == 'Z');
    验证(ftruncate(文件, 2) == 0 && lseek(文件, 0, SEEK_CUR) == 9);
    验证(ftruncate(文件, 6) == 0 && lseek(文件, 2, SEEK_SET) == 2 && read(文件, 数据, 4) == 4);
    验证(!数据[0] && !数据[1] && !数据[2] && !数据[3]);
    验证(lseek(文件, 2147483647, SEEK_SET) == 2147483647);
    验证(lseek(文件, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    验证(lseek(文件, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    验证(write(文件, "!", 1) == -1 && errno == EFBIG);
    验证(lseek(文件, 0, SEEK_SET) == 0);
    验证(read(文件, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    验证(read(文件, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    验证(write(文件, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    验证(read(文件, 数据, (size_t)-1) == -1 && errno == EINVAL);
    验证(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    验证(fstat(文件, (void *)0x00100000) == -1 && errno == EFAULT);
    验证(lseek(文件, 0, SEEK_CUR) == 0);
    验证(read(文件, NULL, 0) == 0 && write(文件, NULL, 0) == 0);
    验证(移除文件条目名称("posix.txt") == 0);
    验证(fstat(文件, &状态值) == 0 && 状态值.st_nlink == 0 && 状态值.st_size == 6);
    int 新建文件 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    验证(新建文件 == 5 && fstat(新建文件, &状态值) == 0 && 状态值.st_size == 0);
    验证(read(文件, 数据, 2) == 2 && memcmp(数据, "ab", 2) == 0);
    验证(close(文件) == 0 && close(克隆值) == 0 && close(新建文件) == 0);
    验证(close(新建文件) == -1 && errno == EBADF);
    验证(unlink("posix.txt") == 0);
    文件 = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    验证(文件 == 3 && fcntl(文件, F_GETFD) == 1);
    验证(read(文件, 数据, 1) == -1 && errno == EBADF);
    验证(write(文件, "keep", 4) == 4);
    for (int 编号 = 4; 编号 < 32; 编号++) 验证(dup(文件) == 编号);
    验证(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    验证(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    验证(fstat(文件, &状态值) == 0 && 状态值.st_size == 4);
    for (int 编号 = 3; 编号 < 32; 编号++) 验证(close(编号) == 0);
    验证(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    文件 = open("posix.txt", O_RDONLY);
    验证(文件 == 3 && write(文件, 数据, 1) == -1 && errno == EBADF);
    验证(fcntl(文件, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    验证(close(8) == 0 && close(文件) == 0 && unlink("posix.txt") == 0);
    验证(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    验证(fstat(1, &状态值) == 0 && S_ISCHR(状态值.st_mode));
    验证(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    验证(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr 地址; char 地址文本[16];
    验证(inet_pton(AF_INET, "10.0.2.2", &地址) == 1 && ntohl(地址.s_addr) == 0x0a000202U);
    验证(inet_ntop(AF_INET, &地址, 地址文本, sizeof 地址文本) == 地址文本 && strcmp(地址文本, "10.0.2.2") == 0);
    验证(inet_pton(AF_INET, "256.0.0.1", &地址) == 0 && ntohl(地址.s_addr) == 0x0a000202U);
    验证(inet_pton(AF_INET, "01.0.0.1", &地址) == 0);
    验证(inet_ntop(AF_INET, &地址, 地址文本, 3) == NULL && errno == ENOSPC);
    验证(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 保留值[8], 项目个数 = 0; char 名称[] = "slot0";
    for (int 编号 = 0; 编号 < 8; 编号++) {
        名称[4] = '0' + 编号;
        int 已打开文件 = open(名称, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (已打开文件 < 0) { 验证(errno == ENOSPC); break; }
        保留值[项目个数++] = 已打开文件;
    }
    验证(项目个数 > 0 && 项目个数 < 8);
    验证(unlink("slot0") == 0);
    验证(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    验证(close(保留值[0]) == 0);
    文件 = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    验证(文件 >= 0 && close(文件) == 0 && unlink("held-slot") == 0);
    for (int 编号 = 1; 编号 < 项目个数; 编号++) {
        名称[4] = '0' + 编号;
        验证(close(保留值[编号]) == 0 && unlink(名称) == 0);
    }
    验证(fsync(-1) == -1 && errno == EBADF);
    验证(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
