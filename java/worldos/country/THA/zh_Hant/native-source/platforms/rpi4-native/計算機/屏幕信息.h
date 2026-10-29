#ifndef 原生屏幕信息標頭
#define 原生屏幕信息標頭
#include <stdint.h>
/* 초기화가 끝난 實際資料 RGB32 屏幕 大小. 준비되지 않았으면 0이다. */
uintptr_t 板屏幕寬度(void);
uintptr_t 板屏幕高度(void);
/* 0: 隱藏值, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 板指針(int 水平位置, int 垂直位置, unsigned 形狀值);
/* 한 번에 32줄을 완성한 後端值, 달라진 화소만 實際資料 화면에 옮긴다. */
void 板準備繪圖(volatile uint32_t *資料, unsigned 寬度跨度, unsigned 長度, unsigned 行間距值);
int 板繪圖邊界(int *水平位置, int *垂直位置, int *寬度跨度, int *長度);
int 板開始繪圖(int 水平位置, int 垂直位置, int 寬度跨度, int 長度);
void 板結束操作繪圖(void);
void 板矩形填充(int 水平位置, int 垂直位置, int 寬度跨度, int 長度, uint32_t 顏色值);
/* 實際資料 顯示值 메모리에 기록한 像素 數. 指針 갱신은 제외한다. */
uint64_t 板繪圖個數(void);
uint32_t 板讀取屏幕(unsigned 水平位置, unsigned 垂直位置);
#endif
