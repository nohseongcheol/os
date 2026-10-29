#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 avvia 라이브러리가 effettivo_dati 프레임버퍼/단조 clock SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int Disegno_rettangolo(unsigned 가로,unsigned Verticale_funzione,unsigned 너비,unsigned altezza_VALORE,unsigned 색상);
unsigned 밀리초(void);
int 그림기다리기(void);
int 화면너비(void);
int schermata_altezza(void);
#endif
