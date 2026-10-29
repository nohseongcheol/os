#include <檔案ABI.h>
#include "呼叫邊界位置.h"

int 錯誤編號;
int 調用狀態結果(int 結果) {
    if (結果 < 0) { 錯誤編號 = -結果; return -1; }
    return 結果;
}
int open(const char *檔案條目名稱, int 打開設置, ...) {
    mode_t 授權權限 = 0;
    if (打開設置 & O_CREAT) {
        __builtin_va_list 實參;
        __builtin_va_start(實參, 打開設置);
        授權權限 = __builtin_va_arg(實參, mode_t);
        __builtin_va_end(實參);
    }
    return 調用狀態結果(jkoros_syscall(30, (int)檔案條目名稱, 打開設置, 授權權限, 0, 0));
}
int creat(const char *檔案條目名稱, mode_t 授權權限) { return open(檔案條目名稱, O_WRONLY | O_CREAT | O_TRUNC, 授權權限); }
ssize_t read(int 檔案描述符, void *資料, size_t 位元組個數) {
    return 調用狀態結果(jkoros_syscall(31, 檔案描述符, (int)資料, 位元組個數, 0, 0));
}
ssize_t write(int 檔案描述符, const void *資料, size_t 位元組個數) {
    return 調用狀態結果(jkoros_syscall(32, 檔案描述符, (int)資料, 位元組個數, 0, 0));
}
int close(int 檔案描述符) { return 調用狀態結果(jkoros_syscall(33, 檔案描述符, 0, 0, 0, 0)); }
off_t lseek(int 檔案描述符, off_t 偏移值, int 項目根) {
    return 調用狀態結果(jkoros_syscall(34, 檔案描述符, 偏移值, 項目根, 0, 0));
}
int dup(int 檔案描述符) { return 調用狀態結果(jkoros_syscall(35, 檔案描述符, 0, 0, 0, 0)); }
int dup2(int 檔案描述符, int 新建描述符) { return 調用狀態結果(jkoros_syscall(36, 檔案描述符, 新建描述符, 0, 0, 0)); }
int fstat(int 檔案描述符, struct stat *狀態值) { return 調用狀態結果(jkoros_syscall(37, 檔案描述符, (int)狀態值, 0, 0, 0)); }
int unlink(const char *檔案條目名稱) { return 調用狀態結果(jkoros_syscall(38, (int)檔案條目名稱, 0, 0, 0, 0)); }
int ftruncate(int 檔案描述符, off_t 位元組個數) { return 調用狀態結果(jkoros_syscall(39, 檔案描述符, 位元組個數, 0, 0, 0)); }
int fsync(int 檔案描述符) { return 調用狀態結果(jkoros_syscall(47, 檔案描述符, 0, 0, 0, 0)); }
int fcntl(int 檔案描述符, int 命令, ...) {
    int 值 = 0;
    if (命令 == F_DUPFD || 命令 == F_DUPFD_CLOEXEC || 命令 == F_SETFD || 命令 == F_SETFL) {
        __builtin_va_list 實參;
        __builtin_va_start(實參, 命令); 值 = __builtin_va_arg(實參, int); __builtin_va_end(實參);
    }
    return 調用狀態結果(jkoros_syscall(40, 檔案描述符, 命令, 值, 0, 0));
}
