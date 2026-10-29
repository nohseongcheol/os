#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 Uruchom_2 라이브러리가 rzeczywisty_dane 프레임버퍼/단조 Zegar SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int rysować_prostokąt(unsigned 가로,unsigned gałąź_stanowisko,unsigned 너비,unsigned wysokość_WARTOŚĆ,unsigned 색상);
unsigned 밀리초(void);
int 그림기다리기(void);
int 화면너비(void);
int 화면높이(void);
#endif
