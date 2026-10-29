#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 起動処理 라이브러리가 実際データ 프레임버퍼/단조 時計 SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int 矩形描画処理(unsigned 水平位置,unsigned 垂直位置,unsigned 幅値,unsigned 高さ値,unsigned 画素色);
unsigned ミリ秒(void);
int 対象描画中待合(void);
int 画面幅(void);
int 画面高さ(void);
#endif
