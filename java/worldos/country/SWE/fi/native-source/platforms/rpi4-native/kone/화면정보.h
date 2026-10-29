#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 todellinen_data RGB32 화면 Koko. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Piilotettu_ARVO, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Taulu_osoitin(int 가로, int toimiala_toimi, unsigned muoto_ARVO_f1cd655a);
/* 한 번에 32줄을 완성한 BACK_ARVO, 달라진 화소만 todellinen_data 화면에 옮긴다. */
void Taulu_Valmistele_piirustus(volatile uint32_t *data, unsigned 폭, unsigned kesto_ARVO, unsigned riviväli_ARVO);
int 보드그림범위(int *가로, int *toimiala_toimi, int *폭, int *kesto_ARVO);
int Taulu_alku_piirustus(int 가로, int toimiala_toimi, int 폭, int kesto_ARVO);
void Taulu_loppu_piirustus(void);
void Taulu_suorakulmio_täyttö(int 가로, int toimiala_toimi, int 폭, int kesto_ARVO, uint32_t 색);
/* todellinen_data näyttää_ARVO 메모리에 기록한 kuvapiste numero. osoitin 갱신은 제외한다. */
uint64_t Taulu_piirustus_LASKE(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned toimiala_toimi);
#endif
