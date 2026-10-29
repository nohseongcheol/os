#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 ausführenVorgang 라이브러리가 tatsächlichDaten 프레임버퍼/단조 Uhr SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int rechteckZeichnen(unsigned waagerechtPosition,unsigned senkrechtPosition,unsigned breiteWert,unsigned höheWert,unsigned bildpunktFarbe);
unsigned millisekunden(void);
int fürZeichnungWarten(void);
int bildschirmBreite(void);
int bildschirmHöhe(void);
#endif
