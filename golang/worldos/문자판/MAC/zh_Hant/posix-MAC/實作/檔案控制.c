#include <檔案控制.h>
#include <系統/系統呼叫.h>

enum { 系統呼叫_開啟 = 5, 系統呼叫_建立檔案 = 8, 系統呼叫_控制檔案 = 55 };

int 開啟(const char *路徑, int 開啟選項, ...)
{
    檔案模式型別 存取方式 = 0;
    if ((開啟選項 & 不存在則建立) != 0) {
        __builtin_va_list 可變引數;
        __builtin_va_start(可變引數, 開啟選項);
        存取方式 = __builtin_va_arg(可變引數, 檔案模式型別);
        __builtin_va_end(可變引數);
    }
    return (int)__syscall_result(
        __syscall6(系統呼叫_開啟, (long)路徑, 開啟選項, 存取方式, 0, 0, 0));
}

int 建立檔案(const char *路徑, 檔案模式型別 存取方式)
{
    return (int)__syscall_result(
        __syscall6(系統呼叫_建立檔案, (long)路徑, 存取方式, 0, 0, 0, 0));
}

int 控制檔案(int 檔案描述編號, int 控制命令, ...)
{
    long 引數值 = 0;
    if (控制命令 == 複製描述編號 || 控制命令 == 設定描述編號旗標 || 控制命令 == 設定檔案狀態旗標) {
        __builtin_va_list 可變引數;
        __builtin_va_start(可變引數, 控制命令);
        引數值 = __builtin_va_arg(可變引數, long);
        __builtin_va_end(可變引數);
    }
    return (int)__syscall_result(
        __syscall6(系統呼叫_控制檔案, 檔案描述編號, 控制命令, 引數值, 0, 0, 0));
}
