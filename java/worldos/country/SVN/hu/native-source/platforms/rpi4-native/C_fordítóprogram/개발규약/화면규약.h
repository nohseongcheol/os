#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 Futtatás 라이브러리가 tényleges_adat 프레임버퍼/단조 Óra SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int Rajz_téglalap(unsigned 가로,unsigned szektor_pozíció,unsigned 너비,unsigned 높이,unsigned 색상);
unsigned 밀리초(void);
int 그림기다리기(void);
int 화면너비(void);
int 화면높이(void);
#endif
