#include "../命名/計算機連接名稱列.h"
#include "調用.h"
extern int main(int,char **);
static char 實際參數陣列[8][256];
int 用戶開始(int 未使用){
    (void)未使用;char *實際參數列表[9];int 參數列個數=用戶調用(15,UINTPTR_MAX,0,0,0,0,0);
    if(參數列個數<0||參數列個數>8)return 126;
    for(int 序數索引=0;序數索引<參數列個數;序數索引++){if(用戶調用(15,序數索引,(uintptr_t)實際參數陣列[序數索引],256,0,0,0)<0)return 126;實際參數列表[序數索引]=實際參數陣列[序數索引];}實際參數列表[參數列個數]=0;
    return main(參數列個數,實際參數列表);
}
void *memset(void*資料位置,int 字元程式碼,size_t 項目個數){unsigned char*目的地址資料=資料位置;while(項目個數--)*目的地址資料++=字元程式碼;return 資料位置;}
void *memcpy(void*目的地址資料,const void*字符串資料,size_t 項目個數){unsigned char*首位值=目的地址資料;const unsigned char*第二值=字符串資料;while(項目個數--)*首位值++=*第二值++;return 目的地址資料;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned 橫座標座標,unsigned Y_按鈕座標,unsigned 寬度值,unsigned 高度值,unsigned 像素顏色){return 屏幕矩形(橫座標座標,Y_按鈕座標,寬度值,高度值,像素顏色);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 用戶調用(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 等待狀態用於屏幕鍵();}
int 繪製矩形(unsigned 水平位置,unsigned 垂直位置,unsigned 寬度值,unsigned 高度值,unsigned 像素顏色){return pk_rectangle(水平位置,垂直位置,寬度值,高度值,像素顏色);}
unsigned 毫秒(void){return pk_ticks_ms();}
int 等待狀態用於繪圖(void){return pk_graphics_wait();}
int 屏幕寬度(void){return 讀取屏幕寬度();}
int 屏幕高度(void){return 讀取屏幕高度();}
