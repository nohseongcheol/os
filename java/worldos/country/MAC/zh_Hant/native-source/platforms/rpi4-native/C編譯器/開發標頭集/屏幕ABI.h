#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 運行 라이브러리가 實際資料 프레임버퍼/단조 時鐘 SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int 繪製矩形(unsigned 水平位置,unsigned 垂直位置,unsigned 寬度值,unsigned 高度值,unsigned 像素顏色);
unsigned 毫秒(void);
int 等待狀態用於繪圖(void);
int 屏幕寬度(void);
int 屏幕高度(void);
#endif
