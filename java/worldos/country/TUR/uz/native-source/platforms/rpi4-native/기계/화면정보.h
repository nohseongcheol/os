#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 real_ma_lumotlar RGB32 화면 Hajmi. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: yashirin_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void yozuv_taxtasi_kursor(int 가로, int Vertikal_holat, unsigned shakl_VALUE);
/* 한 번에 32줄을 완성한 Orqaga_VALUE, 달라진 화소만 real_ma_lumotlar 화면에 옮긴다. */
void yozuv_taxtasi_Tayyorlamoq_chizish(volatile uint32_t *ma_lumotlar, unsigned 폭, unsigned uzunlik_VALUE, unsigned yetakchi_VALUE);
int 보드그림범위(int *가로, int *Vertikal_holat, int *폭, int *uzunlik_VALUE);
int yozuv_taxtasi_Start_chizish(int 가로, int Vertikal_holat, int 폭, int uzunlik_VALUE);
void yozuv_taxtasi_Tugatmoq_chizish(void);
void 보드사각그림(int 가로, int Vertikal_holat, int 폭, int uzunlik_VALUE, uint32_t 색);
/* real_ma_lumotlar ko_rsatmoq_VALUE 메모리에 기록한 piksel 수. kursor 갱신은 제외한다. */
uint64_t yozuv_taxtasi_chizish_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikal_holat);
#endif
