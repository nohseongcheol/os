/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣告_系統_通訊端點
#define _宣告_系統_通訊端點

#include <基本定義.h>
#include <系統/資料型別.h>

typedef unsigned short 位址族型別;

struct 通訊端點位址 {
    位址族型別 端點位址族;
    char 位址資料[14];
};

#define 未指定位址族 0
#define 互聯網路位址族 2
#define 互聯網路協定族 互聯網路位址族

#define 資料流端點 1
#define 資料報端點 2

#define 停止接收 0
#define 停止傳送 1
#define 停止雙向通訊 2

#ifdef __cplusplus
extern "C" {
#endif
int 建立通訊端點(int 位址族, int 端點類型, int 通訊協定);
int 繫結本地位址(int 檔案描述編號, const struct 通訊端點位址 *位址, 位址長度型別 位址大小);
int 連接對端(int 檔案描述編號, const struct 通訊端點位址 *位址, 位址長度型別 位址大小);
int 準備接收連線(int 檔案描述編號, int 等待上限);
int 接受連線(int 檔案描述編號, struct 通訊端點位址 *位址, 位址長度型別 *位址大小);
int 取得本地端點位址(int 檔案描述編號, struct 通訊端點位址 *位址, 位址長度型別 *位址大小);
int 取得對端位址(int 檔案描述編號, struct 通訊端點位址 *位址, 位址長度型別 *位址大小);
有號大小型別 傳送(int 檔案描述編號, const void *資料緩衝區域, 大小型別 長度, int 處理旗標);
有號大小型別 接收(int 檔案描述編號, void *資料緩衝區域, 大小型別 長度, int 處理旗標);
有號大小型別 向目的位址傳送(int 檔案描述編號, const void *訊息, 大小型別 長度, int 處理旗標,
               const struct 通訊端點位址 *目的位址, 位址長度型別 目的位址長度);
有號大小型別 接收並取得來源位址(int 檔案描述編號, void *資料緩衝區域, 大小型別 長度, int 處理旗標,
                 struct 通訊端點位址 *位址, 位址長度型別 *位址大小);
int 關閉通訊方向(int 檔案描述編號, int 關閉方向);
int 設定通訊端點選項(int 檔案描述編號, int 設定層級, int 選項名稱,
               const void *選項值, 位址長度型別 選項長度);
#ifdef __cplusplus
}
#endif

#endif
