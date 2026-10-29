#include "../命名/計算機連接名稱列.h"
#include "../計算機/屏幕信息.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 內核致命停止(const char *說明){fputs(說明,stderr);abort();}
extern uintptr_t 板終端(uintptr_t),板像素(uintptr_t,uintptr_t,uintptr_t);
extern void 終端指針(unsigned,int,int),終端位元組(unsigned);
extern int 調用屏幕(int,unsigned,int,int,int,int,int);
static uint32_t 屏幕[1080][1936],比較映像[1080][1936];
uintptr_t 板幀緩衝(void){return 1;}
static void 比較整體(void){
    板指針(0,0,0);memcpy(比較映像,屏幕,sizeof(屏幕));
    uint64_t 上一個項目=板繪圖個數();板終端(3);
    assert(memcmp(比較映像,屏幕,sizeof(屏幕))==0);
    assert(板繪圖個數()==上一個項目); /* 같은 화면을 重試值 그려도 顯示值 메모리에 쓰지 않는다. */
}
static void 寫入文本(const char *文本){while(*文本)終端位元組((unsigned char)*文本++);}
int main(void){
    板準備繪圖(&屏幕[0][0],1920,1080,sizeof(屏幕[0]));
    板終端(300);寫入文本("首位項目 창의 한글 資料\n");
    for(int 編號=1;編號<4;編號++){板終端(1);板終端(100+編號);寫入文本("겹친 창의 한글 資料\n\033[41m색칠한 跳過空白     \033[0m\n");}
    比較整體();
    int 水平位置=60,垂直位置=102,寬度跨度=568,高度值=360;
    uint64_t 移動日誌=0;double 移動量時間=0;
    for(int 序列值=0;序列值<80;序列值++){
        終端指針(1,水平位置+100,垂直位置+15);
        int 新建水平位置=80+(序列值*37)%850,新建垂直位置=50+(序列值*13)%450;
        板像素(1900,1050,0x123456); /* 刷新 區域值 밖의 使用者 繪圖 */
        uint64_t 上一個項目=板繪圖個數();clock_t 運行=clock();
        終端指針(1,新建水平位置+100,新建垂直位置+15);
        移動量時間+=(double)(clock()-運行)/CLOCKS_PER_SEC;
        移動日誌+=板繪圖個數()-上一個項目;
        assert(板繪圖個數()-上一個項目<=2u*寬度跨度*高度值);
        assert(屏幕[1050][1900]==0x123456);
        板像素(1900,1050,0x302018);
        終端指針(0,新建水平位置+100,新建垂直位置+15);水平位置=新建水平位置;垂直位置=新建垂直位置;
        比較整體();
    }
    for(int 序列值=0;序列值<40;序列值++){
        int 新建寬度=360+(序列值*29)%700,新建高度=216+(序列值*17)%350;
        if(新建寬度>1920-水平位置)新建寬度=1920-水平位置;if(新建高度>1080-垂直位置)新建高度=1080-垂直位置;
        終端指針(1,水平位置+寬度跨度-4,垂直位置+高度值-4);
        終端指針(1,水平位置+新建寬度-4,垂直位置+新建高度-4);
        uint64_t 上一個項目=板繪圖個數();
        終端指針(1,水平位置+新建寬度-4,垂直位置+新建高度-4);
        assert(板繪圖個數()==上一個項目); /* 같은 좌표의 중복 事件 */
        終端指針(0,水平位置+新建寬度-4,垂直位置+新建高度-4);寬度跨度=新建寬度;高度值=新建高度;
        比較整體();
    }
    /* 已裁剪值 범위와 實際資料 行 간격을 지킨다. */
    for(int 行=0;行<1080;行++)for(int 槽條目=1920;槽條目<1936;槽條目++)assert(屏幕[行][槽條目]==0);
    assert(!板開始繪圖(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",移動量時間*1000/80,(unsigned long long)(移動日誌/80));
    return 0;
}
