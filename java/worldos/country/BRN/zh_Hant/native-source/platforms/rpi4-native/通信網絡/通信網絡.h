#ifndef 原生網路標頭
#define 原生網路標頭
#include <stdint.h>
#include <stddef.h>
void 準備網路(void);
void 審查網路(void);
int 創建通訊端端點(int 類型分類);
int 網路層綁定(int 檔案句柄, uint32_t 地址, unsigned 埠編號);
int 網路層偵聽(int 檔案句柄);
void 複用通訊端地址(int 檔案句柄);
int 網路層連接(int 檔案句柄, uint32_t 地址, unsigned 埠編號);
int 網路層接受(int 檔案句柄);
int 網路層讀取(int 檔案句柄, void *資料, unsigned 項目個數);
int 網路層寫入(int 檔案句柄, const void *資料, unsigned 項目個數);
int 發送數據報(int 檔案句柄, const void *資料, unsigned 項目個數, uint32_t 地址, unsigned 埠編號);
int 接收數據報(int 檔案句柄, void *資料, unsigned 項目個數);
unsigned 網路埠編號(int 檔案句柄);
unsigned 對端埠編號(int 檔案句柄);
uint32_t 網路層對端地址(int 檔案句柄);
void 關閉網路(int 檔案句柄);
int 檔案傳送控制(int 動作);
void 審查檔案傳送(void);
uint32_t 讀取網路運行狀態(unsigned 條目值, unsigned 編號);
int 設定配置網路(unsigned 動作, uint32_t 地址, uint32_t 掩碼值, uint32_t 網關值);
int 開始響應測試(uint32_t 地址, unsigned 排序值);
int 讀取響應測試(unsigned 條目值);
#endif
