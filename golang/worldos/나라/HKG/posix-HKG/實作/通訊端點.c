#include <通訊位址/位元組順序.h>
#include <系統/系統呼叫.h>
#include <系統/通訊端點.h>

enum { 通訊端點系統呼叫編號 = 102 };
enum {
    通訊端點_建立通訊端點 = 1, 通訊端點_繫結本地位址 = 2, 通訊端點_連接對端 = 3, 通訊端點_準備接收連線 = 4,
    通訊端點_接受連線 = 5, 通訊端點_取得本地端點位址 = 6, 通訊端點_取得對端位址 = 7,
    通訊端點_傳送 = 9, 通訊端點_接收 = 10, 通訊端點_向目的位址傳送 = 11, 通訊端點_接收並取得來源位址 = 12,
    通訊端點_關閉通訊方向 = 13, 通訊端點_設定通訊端點選項 = 14
};

static long 呼叫通訊端點(long 通訊呼叫編號, unsigned long *傳入引數列表)
{
    return __syscall_result(
        __syscall6(通訊端點系統呼叫編號, 通訊呼叫編號, (long)傳入引數列表, 0, 0, 0, 0));
}

無號16位整數 轉為網路次序16位(無號16位整數 值) { return (無號16位整數)((值 << 8) | (值 >> 8)); }
無號16位整數 轉為主機次序16位(無號16位整數 值) { return 轉為網路次序16位(值); }
無號32位整數 轉為網路次序32位(無號32位整數 值)
{
    return ((值 & 0x000000ffU) << 24) | ((值 & 0x0000ff00U) << 8) |
           ((值 & 0x00ff0000U) >> 8) | ((值 & 0xff000000U) >> 24);
}
無號32位整數 轉為主機次序32位(無號32位整數 值) { return 轉為網路次序32位(值); }

int 建立通訊端點(int 位址族, int 端點類型, int 通訊協定)
{
    unsigned long 傳值陣列[3] = {(unsigned long)位址族, (unsigned long)端點類型, (unsigned long)通訊協定};
    return (int)呼叫通訊端點(通訊端點_建立通訊端點, 傳值陣列);
}

int 繫結本地位址(int 檔案描述編號, const struct 通訊端點位址 *位址, 位址長度型別 長度)
{
    unsigned long 傳值陣列[3] = {(unsigned long)檔案描述編號, (unsigned long)位址, 長度};
    return (int)呼叫通訊端點(通訊端點_繫結本地位址, 傳值陣列);
}

int 連接對端(int 檔案描述編號, const struct 通訊端點位址 *位址, 位址長度型別 長度)
{
    unsigned long 傳值陣列[3] = {(unsigned long)檔案描述編號, (unsigned long)位址, 長度};
    return (int)呼叫通訊端點(通訊端點_連接對端, 傳值陣列);
}

int 準備接收連線(int 檔案描述編號, int 等待上限)
{
    unsigned long 傳值陣列[2] = {(unsigned long)檔案描述編號, (unsigned long)等待上限};
    return (int)呼叫通訊端點(通訊端點_準備接收連線, 傳值陣列);
}

int 接受連線(int 檔案描述編號, struct 通訊端點位址 *位址, 位址長度型別 *長度)
{
    unsigned long 傳值陣列[3] = {(unsigned long)檔案描述編號, (unsigned long)位址, (unsigned long)長度};
    return (int)呼叫通訊端點(通訊端點_接受連線, 傳值陣列);
}

int 取得本地端點位址(int 檔案描述編號, struct 通訊端點位址 *位址, 位址長度型別 *長度)
{
    unsigned long 傳值陣列[3] = {(unsigned long)檔案描述編號, (unsigned long)位址, (unsigned long)長度};
    return (int)呼叫通訊端點(通訊端點_取得本地端點位址, 傳值陣列);
}

int 取得對端位址(int 檔案描述編號, struct 通訊端點位址 *位址, 位址長度型別 *長度)
{
    unsigned long 傳值陣列[3] = {(unsigned long)檔案描述編號, (unsigned long)位址, (unsigned long)長度};
    return (int)呼叫通訊端點(通訊端點_取得對端位址, 傳值陣列);
}

有號大小型別 傳送(int 檔案描述編號, const void *資料緩衝區域, 大小型別 長度, int 處理旗標)
{
    unsigned long 傳值陣列[4] = {(unsigned long)檔案描述編號, (unsigned long)資料緩衝區域, 長度, (unsigned long)處理旗標};
    return (有號大小型別)呼叫通訊端點(通訊端點_傳送, 傳值陣列);
}

有號大小型別 接收(int 檔案描述編號, void *資料緩衝區域, 大小型別 長度, int 處理旗標)
{
    unsigned long 傳值陣列[4] = {(unsigned long)檔案描述編號, (unsigned long)資料緩衝區域, 長度, (unsigned long)處理旗標};
    return (有號大小型別)呼叫通訊端點(通訊端點_接收, 傳值陣列);
}

有號大小型別 向目的位址傳送(int 檔案描述編號, const void *資料緩衝區域, 大小型別 長度, int 處理旗標,
               const struct 通訊端點位址 *位址, 位址長度型別 位址長度)
{
    unsigned long 傳值陣列[6] = {(unsigned long)檔案描述編號, (unsigned long)資料緩衝區域, 長度,
                          (unsigned long)處理旗標, (unsigned long)位址, 位址長度};
    return (有號大小型別)呼叫通訊端點(通訊端點_向目的位址傳送, 傳值陣列);
}

有號大小型別 接收並取得來源位址(int 檔案描述編號, void *資料緩衝區域, 大小型別 長度, int 處理旗標,
                 struct 通訊端點位址 *位址, 位址長度型別 *位址長度)
{
    unsigned long 傳值陣列[6] = {(unsigned long)檔案描述編號, (unsigned long)資料緩衝區域, 長度,
                          (unsigned long)處理旗標, (unsigned long)位址,
                          (unsigned long)位址長度};
    return (有號大小型別)呼叫通訊端點(通訊端點_接收並取得來源位址, 傳值陣列);
}

int 關閉通訊方向(int 檔案描述編號, int 關閉方向)
{
    unsigned long 傳值陣列[2] = {(unsigned long)檔案描述編號, (unsigned long)關閉方向};
    return (int)呼叫通訊端點(通訊端點_關閉通訊方向, 傳值陣列);
}

int 設定通訊端點選項(int 檔案描述編號, int 設定層級, int 選項名稱,
               const void *選項值, 位址長度型別 選項長度)
{
    unsigned long 傳值陣列[5] = {(unsigned long)檔案描述編號, (unsigned long)設定層級,
                          (unsigned long)選項名稱, (unsigned long)選項值,
                          選項長度};
    return (int)呼叫通訊端點(通訊端點_設定通訊端點選項, 傳值陣列);
}
