#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 stvaran_podaci RGB32 화면 Veličina. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: sakriven_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void pano_pokazivač(int 가로, int Okomito_položaj, unsigned oblik_VALUE_f1cd655a);
/* 한 번에 32줄을 완성한 TRAG_VALUE, 달라진 화소만 stvaran_podaci 화면에 옮긴다. */
void pano_Pripremi_crtež(volatile uint32_t *podaci, unsigned 폭, unsigned 길이, unsigned prored_VALUE);
int 보드그림범위(int *가로, int *Okomito_položaj, int *폭, int *길이);
int pano_START_crtež(int 가로, int Okomito_položaj, int 폭, int 길이);
void pano_Završi_crtež(void);
void pano_pravokutnik_ispuna(int 가로, int Okomito_položaj, int 폭, int 길이, uint32_t 색);
/* stvaran_podaci emisija_VALUE 메모리에 기록한 slikovni_element 수. pokazivač 갱신은 제외한다. */
uint64_t pano_crtež_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Okomito_položaj);
#endif
