/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣告_檔案控制
#define _宣告_檔案控制

#include <系統/資料型別.h>

#define 唯讀開啟 0x0000
#define 唯寫開啟 0x0001
#define 讀寫開啟 0x0002
#define 存取模式遮罩 0x0003
#define 不存在則建立 0x0040
#define 僅允許新檔案 0x0080
#define 清空原有內容 0x0200
#define 在末尾附加 0x0400
#define 僅允許目錄 0x10000

#define 複製描述編號 0
#define 取得描述編號旗標 1
#define 設定描述編號旗標 2
#define 取得檔案狀態旗標 3
#define 設定檔案狀態旗標 4
#define 替換程式時關閉 1

#ifdef __cplusplus
extern "C" {
#endif
int 開啟(const char *路徑, int 開啟選項, ...);
int 建立檔案(const char *路徑, 檔案模式型別 存取方式);
int 控制檔案(int 檔案描述編號, int 控制命令, ...);
#ifdef __cplusplus
}
#endif

#endif
