/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣告_系統_子行程等待
#define _宣告_系統_子行程等待

#include <系統/資料型別.h>

#define 未就緒則不等待 1
#define 提取結束值(結束狀態) (((結束狀態) >> 8) & 0xff)
#define 檢查正常結束(結束狀態) (((結束狀態) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
行程編號型別 等待子行程(int *結束狀態);
行程編號型別 等待指定子行程(行程編號型別 行程編號, int *結束狀態, int 選項);
#ifdef __cplusplus
}
#endif

#endif
