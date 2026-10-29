#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 stvarni_podaci RGB32 화면 promeniti_veličinu. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skriveno_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tabla_pokazivač(int 가로, int vertikala_pozicija, unsigned oblik_VALUE);
/* 한 번에 32줄을 완성한 NAZAD_VALUE, 달라진 화소만 stvarni_podaci 화면에 옮긴다. */
void Tabla_Pripremi_crtež(volatile uint32_t *podaci, unsigned 폭, unsigned 길이, unsigned prored_VALUE);
int 보드그림범위(int *가로, int *vertikala_pozicija, int *폭, int *길이);
int Tabla_START_crtež(int 가로, int vertikala_pozicija, int 폭, int 길이);
void Tabla_kraj_crtež(void);
void 보드사각그림(int 가로, int vertikala_pozicija, int 폭, int 길이, uint32_t 색);
/* stvarni_podaci emisija_VALUE 메모리에 기록한 piksel 수. pokazivač 갱신은 제외한다. */
uint64_t Tabla_crtež_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned vertikala_pozicija);
#endif
