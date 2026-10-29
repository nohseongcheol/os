#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 chạy 라이브러리가 dữLiệuThựcTế 프레임버퍼/단조 ĐồngHồ SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int vẽHìnhChữNhật(unsigned vịTríNgang,unsigned vịTríDọc,unsigned giáTrịRộng,unsigned giáTrịCao,unsigned màuĐiểmẢnh);
unsigned miliGiây(void);
int chờBảnVẽCho(void);
int rộngMànHình(void);
int caoMànHình(void);
#endif
