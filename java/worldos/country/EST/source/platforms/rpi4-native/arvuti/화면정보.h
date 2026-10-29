#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 tegelik_andmed RGB32 화면 Suurus. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Peidetud_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tahvel_kursor(int 가로, int vertikaal_ametikoht, unsigned kujund_VALUE);
/* 한 번에 32줄을 완성한 Tagasi_VALUE, 달라진 화소만 tegelik_andmed 화면에 옮긴다. */
void Tahvel_Ettevalmistamine_joonis(volatile uint32_t *andmed, unsigned 폭, unsigned 길이, unsigned reasamm_VALUE);
int 보드그림범위(int *가로, int *vertikaal_ametikoht, int *폭, int *길이);
int Tahvel_START_joonis(int 가로, int vertikaal_ametikoht, int 폭, int 길이);
void Tahvel_lõpp_joonis(void);
void Tahvel_ristkülik_täide(int 가로, int vertikaal_ametikoht, int 폭, int 길이, uint32_t 색);
/* tegelik_andmed saade_VALUE 메모리에 기록한 piksel number. kursor 갱신은 제외한다. */
uint64_t Tahvel_joonis_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned vertikaal_ametikoht);
#endif
