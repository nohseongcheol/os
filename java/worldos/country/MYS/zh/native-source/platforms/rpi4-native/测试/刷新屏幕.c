#include "../命名/计算机连接名称列.h"
#include "../计算机/屏幕信息.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 内核致命停止(const char *说明){fputs(说明,stderr);abort();}
extern uintptr_t 板终端(uintptr_t),板像素(uintptr_t,uintptr_t,uintptr_t);
extern void 终端指针(unsigned,int,int),终端字节(unsigned);
extern int 调用屏幕(int,unsigned,int,int,int,int,int);
static uint32_t 屏幕[1080][1936],比较映像[1080][1936];
uintptr_t 板帧缓冲(void){return 1;}
static void 比较整体(void){
    板指针(0,0,0);memcpy(比较映像,屏幕,sizeof(屏幕));
    uint64_t 上一个项目=板绘图个数();板终端(3);
    assert(memcmp(比较映像,屏幕,sizeof(屏幕))==0);
    assert(板绘图个数()==上一个项目); /* 같은 화면을 重试值 그려도 显示值 메모리에 쓰지 않는다. */
}
static void 写入文本(const char *文本){while(*文本)终端字节((unsigned char)*文本++);}
int main(void){
    板准备绘图(&屏幕[0][0],1920,1080,sizeof(屏幕[0]));
    板终端(300);写入文本("首位项目 창의 한글 数据\n");
    for(int 编号=1;编号<4;编号++){板终端(1);板终端(100+编号);写入文本("겹친 창의 한글 数据\n\033[41m색칠한 跳过空白     \033[0m\n");}
    比较整体();
    int 水平位置=60,垂直位置=102,宽度跨度=568,高度值=360;
    uint64_t 移动日志=0;double 移动量时间=0;
    for(int 序列值=0;序列值<80;序列值++){
        终端指针(1,水平位置+100,垂直位置+15);
        int 新建水平位置=80+(序列值*37)%850,新建垂直位置=50+(序列值*13)%450;
        板像素(1900,1050,0x123456); /* 刷新 区域值 밖의 用户 绘图 */
        uint64_t 上一个项目=板绘图个数();clock_t 运行=clock();
        终端指针(1,新建水平位置+100,新建垂直位置+15);
        移动量时间+=(double)(clock()-运行)/CLOCKS_PER_SEC;
        移动日志+=板绘图个数()-上一个项目;
        assert(板绘图个数()-上一个项目<=2u*宽度跨度*高度值);
        assert(屏幕[1050][1900]==0x123456);
        板像素(1900,1050,0x302018);
        终端指针(0,新建水平位置+100,新建垂直位置+15);水平位置=新建水平位置;垂直位置=新建垂直位置;
        比较整体();
    }
    for(int 序列值=0;序列值<40;序列值++){
        int 新建宽度=360+(序列值*29)%700,新建高度=216+(序列值*17)%350;
        if(新建宽度>1920-水平位置)新建宽度=1920-水平位置;if(新建高度>1080-垂直位置)新建高度=1080-垂直位置;
        终端指针(1,水平位置+宽度跨度-4,垂直位置+高度值-4);
        终端指针(1,水平位置+新建宽度-4,垂直位置+新建高度-4);
        uint64_t 上一个项目=板绘图个数();
        终端指针(1,水平位置+新建宽度-4,垂直位置+新建高度-4);
        assert(板绘图个数()==上一个项目); /* 같은 좌표의 중복 事件 */
        终端指针(0,水平位置+新建宽度-4,垂直位置+新建高度-4);宽度跨度=新建宽度;高度值=新建高度;
        比较整体();
    }
    /* 已裁剪值 범위와 实际数据 行 간격을 지킨다. */
    for(int 行=0;行<1080;行++)for(int 槽条目=1920;槽条目<1936;槽条目++)assert(屏幕[行][槽条目]==0);
    assert(!板开始绘图(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",移动量时间*1000/80,(unsigned long long)(移动日志/80));
    return 0;
}
