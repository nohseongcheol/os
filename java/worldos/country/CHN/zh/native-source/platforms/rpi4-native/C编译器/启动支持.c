#include "../命名/计算机连接名称列.h"
#include "调用.h"
extern int main(int,char **);
static char 参数数组[8][256];
int 用户开始(int 未使用){
    (void)未使用;char *参数列表[9];int 参数列个数=用户调用(15,UINTPTR_MAX,0,0,0,0,0);
    if(参数列个数<0||参数列个数>8)return 126;
    for(int 序数索引=0;序数索引<参数列个数;序数索引++){if(用户调用(15,序数索引,(uintptr_t)参数数组[序数索引],256,0,0,0)<0)return 126;参数列表[序数索引]=参数数组[序数索引];}参数列表[参数列个数]=0;
    return main(参数列个数,参数列表);
}
void *memset(void*数据位置,int 字符代码,size_t 项目个数){unsigned char*目的地址数据=数据位置;while(项目个数--)*目的地址数据++=字符代码;return 数据位置;}
void *memcpy(void*目的地址数据,const void*字符串数据,size_t 项目个数){unsigned char*首位值=目的地址数据;const unsigned char*第二值=字符串数据;while(项目个数--)*首位值++=*第二值++;return 目的地址数据;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned 横坐标坐标,unsigned Y_按钮坐标,unsigned 宽度值,unsigned 高度值,unsigned 像素颜色){return 屏幕矩形(横坐标坐标,Y_按钮坐标,宽度值,高度值,像素颜色);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 用户调用(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 等待状态用于屏幕键();}
int 绘制矩形(unsigned 水平位置,unsigned 垂直位置,unsigned 宽度值,unsigned 高度值,unsigned 像素颜色){return pk_rectangle(水平位置,垂直位置,宽度值,高度值,像素颜色);}
unsigned 毫秒(void){return pk_ticks_ms();}
int 等待状态用于绘图(void){return pk_graphics_wait();}
int 屏幕宽度(void){return 读取屏幕宽度();}
int 屏幕高度(void){return 读取屏幕高度();}
