#ifndef 原生屏幕信息头部
#define 原生屏幕信息头部
#include <stdint.h>
/* 초기화가 끝난 实际数据 RGB32 屏幕 大小. 준비되지 않았으면 0이다. */
uintptr_t 板屏幕宽度(void);
uintptr_t 板屏幕高度(void);
/* 0: 隐藏值, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 板指针(int 水平位置, int 垂直位置, unsigned 形状值);
/* 한 번에 32줄을 완성한 后端值, 달라진 화소만 实际数据 화면에 옮긴다. */
void 板准备绘图(volatile uint32_t *数据, unsigned 宽度跨度, unsigned 长度, unsigned 行间距值);
int 板绘图边界(int *水平位置, int *垂直位置, int *宽度跨度, int *长度);
int 板开始绘图(int 水平位置, int 垂直位置, int 宽度跨度, int 长度);
void 板结束操作绘图(void);
void 板矩形填充(int 水平位置, int 垂直位置, int 宽度跨度, int 长度, uint32_t 颜色值);
/* 实际数据 显示值 메모리에 기록한 像素 数. 指针 갱신은 제외한다. */
uint64_t 板绘图个数(void);
uint32_t 板读取屏幕(unsigned 水平位置, unsigned 垂直位置);
#endif
