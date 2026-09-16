/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣告_輸入輸出與執行
#define _宣告_輸入輸出與執行

#include <基本定義.h>
#include <系統/資料型別.h>

#define 標準輸入編號 0
#define 標準輸出編號 1
#define 標準錯誤輸出編號 2
#define 檢查存在 0
#define 檢查執行權限 1
#define 檢查寫入權限 2
#define 檢查讀取權限 4
#define 從起點定位 0
#define 從目前位置定位 1
#define 從末尾定位 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **環境變數列表;
void 立即結束(int 結束狀態) __attribute__((noreturn));
有號大小型別 讀取(int 檔案描述編號, void *緩衝區域, 大小型別 數量);
有號大小型別 寫入(int 檔案描述編號, const void *緩衝區域, 大小型別 數量);
int 關閉(int 檔案描述編號);
檔案位置型別 移動讀寫位置(int 檔案描述編號, 檔案位置型別 位移, int 位置基準);
行程編號型別 分出子行程(void);
int 替換執行內容(const char *路徑, char *const 引數列表[], char *const 環境列表[]);
行程編號型別 取得行程編號(void);
行程編號型別 取得父行程編號(void);
使用者編號型別 取得使用者編號(void);
使用者編號型別 取得有效使用者編號(void);
群組編號型別 取得群組編號(void);
群組編號型別 取得有效群組編號(void);
int 檢查存取權限(const char *路徑, int 存取方式);
int 切換工作目錄(const char *路徑);
char *取得工作目錄路徑(char *緩衝區域, 大小型別 大小);
int 複製開啟檔案參照(int 檔案描述編號);
int 按指定編號複製檔案參照(int 原描述編號, int 新描述編號);
int 同步檔案記錄(int 檔案描述編號);
void 同步全部記錄(void);
int 檢查是否終端(int 檔案描述編號);
int 設定動態記憶末端(void *位址);
void *移動動態記憶末端(int 增量);
#ifdef __cplusplus
}
#endif

#endif
