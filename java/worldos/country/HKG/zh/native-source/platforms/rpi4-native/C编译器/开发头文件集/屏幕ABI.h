#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 运行 라이브러리가 实际数据 프레임버퍼/단조 时钟 SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int 绘制矩形(unsigned 水平位置,unsigned 垂直位置,unsigned 宽度值,unsigned 高度值,unsigned 像素颜色);
unsigned 毫秒(void);
int 等待状态用于绘图(void);
int 屏幕宽度(void);
int 屏幕高度(void);
#endif
