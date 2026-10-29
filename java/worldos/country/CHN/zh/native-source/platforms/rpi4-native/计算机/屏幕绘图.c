/* 实际数据 屏幕 메모리와 기존 C 调用 규약만 연결한다. 합성 구현은 源代码/帧缓冲组合器.java. */
#include "../命名/计算机连接名称列.h"
#include "屏幕信息.h"
static volatile uint32_t *像素列列表;
static unsigned 屏幕行机器字个数, 屏幕宽度, 屏幕高度;
extern void Java绘图准备(int,int),Java绘图结束(void),Java绘图矩形(int,int,int,int,int),Java绘图指针(int,int,int);
extern int Java绘图宽度(void),Java绘图高度(void),Java绘图个数低位(void),Java绘图个数高位(void);
extern int Java绘图裁剪(int,int,int,int),Java绘图裁剪值(int),Java绘图开始位置(int,int,int,int),Java绘图像素(int,int,int);
uintptr_t 板帧缓冲读取(uintptr_t 水平位置,uintptr_t 垂直位置){
    return 像素列列表&&水平位置<屏幕宽度&&垂直位置<屏幕高度?像素列列表[垂直位置*屏幕行机器字个数+水平位置]:0;
}
void 板帧缓冲写入(uintptr_t 水平位置,uintptr_t 垂直位置,uintptr_t 颜色值){
    if(像素列列表&&水平位置<屏幕宽度&&垂直位置<屏幕高度)像素列列表[垂直位置*屏幕行机器字个数+水平位置]=(uint32_t)颜色值;
}
void 板准备绘图(volatile uint32_t *数据,unsigned 宽度跨度,unsigned 长度,unsigned 行间距值){
    像素列列表=数据;屏幕宽度=宽度跨度;屏幕高度=长度;屏幕行机器字个数=行间距值/4;Java绘图准备((int)宽度跨度,(int)长度);
}
uintptr_t 板屏幕宽度(void){return (unsigned)Java绘图宽度();}
uintptr_t 板屏幕高度(void){return (unsigned)Java绘图高度();}
uint64_t 板绘图个数(void){return ((uint64_t)(uint32_t)Java绘图个数高位()<<32)|(uint32_t)Java绘图个数低位();}
uint32_t 板读取屏幕(unsigned 水平位置,unsigned 垂直位置){return (uint32_t)板帧缓冲读取(水平位置,垂直位置);}
int 板绘图边界(int *水平位置,int *垂直位置,int *宽度跨度,int *长度){
    if(!Java绘图裁剪(*水平位置,*垂直位置,*宽度跨度,*长度))return 0;
    *水平位置=Java绘图裁剪值(0);*垂直位置=Java绘图裁剪值(1);*宽度跨度=Java绘图裁剪值(2);*长度=Java绘图裁剪值(3);return 1;
}
int 板开始绘图(int 水平位置,int 垂直位置,int 宽度跨度,int 长度){return Java绘图开始位置(水平位置,垂直位置,宽度跨度,长度);}
void 板结束操作绘图(void){Java绘图结束();}
uintptr_t 板像素(uintptr_t 水平位置,uintptr_t 垂直位置,uintptr_t 颜色值){return (unsigned)Java绘图像素((int)水平位置,(int)垂直位置,(int)颜色值);}
void 板矩形填充(int 水平位置,int 垂直位置,int 宽度跨度,int 长度,uint32_t 颜色值){Java绘图矩形(水平位置,垂直位置,宽度跨度,长度,(int)颜色值);}
void 板指针(int 水平位置,int 垂直位置,unsigned 形状值){Java绘图指针(水平位置,垂直位置,(int)形状值);}
