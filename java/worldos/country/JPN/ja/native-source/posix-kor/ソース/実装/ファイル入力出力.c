#include <ファイルABI.h>
#include "呼出し境界位置.h"

int エラー番号;
int 呼出状態結果(int 結果) {
    if (結果 < 0) { エラー番号 = -結果; return -1; }
    return 結果;
}
int open(const char *ファイル入口名前, int 設定値開放, ...) {
    mode_t 許可許可権 = 0;
    if (設定値開放 & O_CREAT) {
        __builtin_va_list 引数;
        __builtin_va_start(引数, 設定値開放);
        許可許可権 = __builtin_va_arg(引数, mode_t);
        __builtin_va_end(引数);
    }
    return 呼出状態結果(jkoros_syscall(30, (int)ファイル入口名前, 設定値開放, 許可許可権, 0, 0));
}
int creat(const char *ファイル入口名前, mode_t 許可許可権) { return open(ファイル入口名前, O_WRONLY | O_CREAT | O_TRUNC, 許可許可権); }
ssize_t read(int ファイル記述子, void *データ, size_t バイト個数) {
    return 呼出状態結果(jkoros_syscall(31, ファイル記述子, (int)データ, バイト個数, 0, 0));
}
ssize_t write(int ファイル記述子, const void *データ, size_t バイト個数) {
    return 呼出状態結果(jkoros_syscall(32, ファイル記述子, (int)データ, バイト個数, 0, 0));
}
int close(int ファイル記述子) { return 呼出状態結果(jkoros_syscall(33, ファイル記述子, 0, 0, 0, 0)); }
off_t lseek(int ファイル記述子, off_t 変位量値, int 計画根) {
    return 呼出状態結果(jkoros_syscall(34, ファイル記述子, 変位量値, 計画根, 0, 0));
}
int dup(int ファイル記述子) { return 呼出状態結果(jkoros_syscall(35, ファイル記述子, 0, 0, 0, 0)); }
int dup2(int ファイル記述子, int 新規記述子) { return 呼出状態結果(jkoros_syscall(36, ファイル記述子, 新規記述子, 0, 0, 0)); }
int fstat(int ファイル記述子, struct stat *状況値) { return 呼出状態結果(jkoros_syscall(37, ファイル記述子, (int)状況値, 0, 0, 0)); }
int unlink(const char *ファイル入口名前) { return 呼出状態結果(jkoros_syscall(38, (int)ファイル入口名前, 0, 0, 0, 0)); }
int ftruncate(int ファイル記述子, off_t バイト個数) { return 呼出状態結果(jkoros_syscall(39, ファイル記述子, バイト個数, 0, 0, 0)); }
int fsync(int ファイル記述子) { return 呼出状態結果(jkoros_syscall(47, ファイル記述子, 0, 0, 0, 0)); }
int fcntl(int ファイル記述子, int 命令, ...) {
    int 値 = 0;
    if (命令 == F_DUPFD || 命令 == F_DUPFD_CLOEXEC || 命令 == F_SETFD || 命令 == F_SETFL) {
        __builtin_va_list 引数;
        __builtin_va_start(引数, 命令); 値 = __builtin_va_arg(引数, int); __builtin_va_end(引数);
    }
    return 呼出状態結果(jkoros_syscall(40, ファイル記述子, 命令, 値, 0, 0));
}
