#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 lancer 라이브러리가 donnéesEffectif 프레임버퍼/단조 Horloge SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int dessinerRectangle(unsigned positionHorizontal,unsigned positionVertical,unsigned valeurLargeur,unsigned valeurHauteur,unsigned couleurPixel);
unsigned millisecondes(void);
int attendreDessinPour(void);
int largeurÉcran(void);
int hauteurÉcran(void);
#endif
