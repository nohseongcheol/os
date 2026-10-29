#include <系統/檔案狀態.h>
#include <系統/系統身分.h>
#include <系統/系統呼叫.h>

enum { 系統呼叫_檔案狀態 = 106, 系統呼叫_取得連結自身狀態 = 107, 系統呼叫_取得開啟檔案狀態 = 108, 系統呼叫_取得系統資訊 = 122 };

int 檔案狀態(const char *路徑, struct 檔案狀態 *緩衝區域)
{
    return (int)__syscall_result(
        __syscall6(系統呼叫_檔案狀態, (long)路徑, (long)緩衝區域, 0, 0, 0, 0));
}

int 取得連結自身狀態(const char *路徑, struct 檔案狀態 *緩衝區域)
{
    return (int)__syscall_result(
        __syscall6(系統呼叫_取得連結自身狀態, (long)路徑, (long)緩衝區域, 0, 0, 0, 0));
}

int 取得開啟檔案狀態(int 檔案描述編號, struct 檔案狀態 *緩衝區域)
{
    return (int)__syscall_result(
        __syscall6(系統呼叫_取得開啟檔案狀態, 檔案描述編號, (long)緩衝區域, 0, 0, 0, 0));
}

int 取得系統資訊(struct 系統身分資訊 *系統資料)
{
    return (int)__syscall_result(
        __syscall6(系統呼叫_取得系統資訊, (long)系統資料, 0, 0, 0, 0, 0));
}
