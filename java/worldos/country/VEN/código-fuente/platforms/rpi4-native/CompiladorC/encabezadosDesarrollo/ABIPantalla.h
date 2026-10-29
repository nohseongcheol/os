#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 ponerEnMarcha 라이브러리가 datosEfectivo 프레임버퍼/단조 Reloj SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int dibujarRectángulo(unsigned posiciónHorizontal,unsigned posiciónVertical,unsigned valorAnchura,unsigned valorAltura,unsigned colorPíxel);
unsigned milisegundos(void);
int esperarDibujoPara(void);
int anchuraPantalla(void);
int alturaPantalla(void);
#endif
