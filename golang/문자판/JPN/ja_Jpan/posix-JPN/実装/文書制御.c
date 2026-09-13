#include <文書制御.h>
#include <体系/体系呼出.h>

enum { 体系呼出_開く = 5, 体系呼出_文書を作る = 8, 体系呼出_文書を制御する = 55 };

int 開く(const char *経路, int 開く際の指定, ...)
{
    文書方式型 利用方式 = 0;
    if ((開く際の指定 & 無ければ作る) != 0) {
        __builtin_va_list 可変引数;
        __builtin_va_start(可変引数, 開く際の指定);
        利用方式 = __builtin_va_arg(可変引数, 文書方式型);
        __builtin_va_end(可変引数);
    }
    return (int)__syscall_result(
        __syscall6(体系呼出_開く, (long)経路, 開く際の指定, 利用方式, 0, 0, 0));
}

int 文書を作る(const char *経路, 文書方式型 利用方式)
{
    return (int)__syscall_result(
        __syscall6(体系呼出_文書を作る, (long)経路, 利用方式, 0, 0, 0, 0));
}

int 文書を制御する(int 文書記述番号, int 制御命令, ...)
{
    long 引数値 = 0;
    if (制御命令 == 記述番号複製 || 制御命令 == 記述番号標識設定 || 制御命令 == 文書状態標識設定) {
        __builtin_va_list 可変引数;
        __builtin_va_start(可変引数, 制御命令);
        引数値 = __builtin_va_arg(可変引数, long);
        __builtin_va_end(可変引数);
    }
    return (int)__syscall_result(
        __syscall6(体系呼出_文書を制御する, 文書記述番号, 制御命令, 引数値, 0, 0, 0));
}
