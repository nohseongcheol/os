/* 實際資料 屏幕 메모리와 기존 C 調用 규약만 연결한다. 합성 구현은 原始碼/幀緩衝組合器.java. */
#include "../命名/計算機連接名稱列.h"
#include "屏幕信息.h"
static volatile uint32_t *像素列列表;
static unsigned 屏幕列機器字個數, 屏幕寬度, 屏幕高度;
extern void Java繪圖準備(int,int),Java繪圖結束(void),Java繪圖矩形(int,int,int,int,int),Java繪圖指針(int,int,int);
extern int Java繪圖寬度(void),Java繪圖高度(void),Java繪圖個數低位(void),Java繪圖個數高位(void);
extern int Java繪圖裁剪(int,int,int,int),Java繪圖裁剪值(int),Java繪圖開始位置(int,int,int,int),Java繪圖像素(int,int,int);
uintptr_t 板幀緩衝讀取(uintptr_t 水平位置,uintptr_t 垂直位置){
    return 像素列列表&&水平位置<屏幕寬度&&垂直位置<屏幕高度?像素列列表[垂直位置*屏幕列機器字個數+水平位置]:0;
}
void 板幀緩衝寫入(uintptr_t 水平位置,uintptr_t 垂直位置,uintptr_t 顏色值){
    if(像素列列表&&水平位置<屏幕寬度&&垂直位置<屏幕高度)像素列列表[垂直位置*屏幕列機器字個數+水平位置]=(uint32_t)顏色值;
}
void 板準備繪圖(volatile uint32_t *資料,unsigned 寬度跨度,unsigned 長度,unsigned 行間距值){
    像素列列表=資料;屏幕寬度=寬度跨度;屏幕高度=長度;屏幕列機器字個數=行間距值/4;Java繪圖準備((int)寬度跨度,(int)長度);
}
uintptr_t 板屏幕寬度(void){return (unsigned)Java繪圖寬度();}
uintptr_t 板屏幕高度(void){return (unsigned)Java繪圖高度();}
uint64_t 板繪圖個數(void){return ((uint64_t)(uint32_t)Java繪圖個數高位()<<32)|(uint32_t)Java繪圖個數低位();}
uint32_t 板讀取屏幕(unsigned 水平位置,unsigned 垂直位置){return (uint32_t)板幀緩衝讀取(水平位置,垂直位置);}
int 板繪圖邊界(int *水平位置,int *垂直位置,int *寬度跨度,int *長度){
    if(!Java繪圖裁剪(*水平位置,*垂直位置,*寬度跨度,*長度))return 0;
    *水平位置=Java繪圖裁剪值(0);*垂直位置=Java繪圖裁剪值(1);*寬度跨度=Java繪圖裁剪值(2);*長度=Java繪圖裁剪值(3);return 1;
}
int 板開始繪圖(int 水平位置,int 垂直位置,int 寬度跨度,int 長度){return Java繪圖開始位置(水平位置,垂直位置,寬度跨度,長度);}
void 板結束操作繪圖(void){Java繪圖結束();}
uintptr_t 板像素(uintptr_t 水平位置,uintptr_t 垂直位置,uintptr_t 顏色值){return (unsigned)Java繪圖像素((int)水平位置,(int)垂直位置,(int)顏色值);}
void 板矩形填充(int 水平位置,int 垂直位置,int 寬度跨度,int 長度,uint32_t 顏色值){Java繪圖矩形(水平位置,垂直位置,寬度跨度,長度,(int)顏色值);}
void 板指針(int 水平位置,int 垂直位置,unsigned 形狀值){Java繪圖指針(水平位置,垂直位置,(int)形狀值);}
