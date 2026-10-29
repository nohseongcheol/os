#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 faktiki_verilənlər RGB32 화면 Böyüklük. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: gizli_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void lövhə_göstərici(int 가로, int Şaquli_yerinə_qoymaq, unsigned fiqur_VALUE);
/* 한 번에 32줄을 완성한 GERİ_VALUE, 달라진 화소만 faktiki_verilənlər 화면에 옮긴다. */
void lövhə_Hazırla_rəsm(volatile uint32_t *verilənlər, unsigned 폭, unsigned uzunluq_VALUE, unsigned aparıcı_VALUE);
int 보드그림범위(int *가로, int *Şaquli_yerinə_qoymaq, int *폭, int *uzunluq_VALUE);
int lövhə_Başla_rəsm(int 가로, int Şaquli_yerinə_qoymaq, int 폭, int uzunluq_VALUE);
void lövhə_Bitir_rəsm(void);
void 보드사각그림(int 가로, int Şaquli_yerinə_qoymaq, int 폭, int uzunluq_VALUE, uint32_t 색);
/* faktiki_verilənlər göstərmək_VALUE 메모리에 기록한 piksel 수. göstərici 갱신은 제외한다. */
uint64_t lövhə_rəsm_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Şaquli_yerinə_qoymaq);
#endif
