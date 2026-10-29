#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 iniciar 라이브러리가 real_dados 프레임버퍼/단조 Relógio SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int emitir_retângulo(unsigned 가로,unsigned Vertical_cargo,unsigned 너비,unsigned altura_VALOR,unsigned 색상);
unsigned 밀리초(void);
int 그림기다리기(void);
int 화면너비(void);
int tela_altura(void);
#endif
