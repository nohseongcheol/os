#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 starten 라이브러리가 werkelijk_gegevens 프레임버퍼/단조 Klok SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int Tekenen_rechthoek(unsigned 가로,unsigned Verticaal_functie,unsigned 너비,unsigned hoogte_WAARDE,unsigned 색상);
unsigned 밀리초(void);
int 그림기다리기(void);
int 화면너비(void);
int scherm_hoogte(void);
#endif
