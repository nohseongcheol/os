#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 real_date RGB32 화면 Mărime. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Ascunsă_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Avizier_cursor(int 가로, int Verticală_poziție, unsigned formă_VALUE);
/* 한 번에 32줄을 완성한 ÎNAPOI_VALUE, 달라진 화소만 real_date 화면에 옮긴다. */
void Avizier_Pregătiți_desen(volatile uint32_t *date, unsigned 폭, unsigned lungime_VALUE, unsigned spațiere_VALUE);
int 보드그림범위(int *가로, int *Verticală_poziție, int *폭, int *lungime_VALUE);
int Avizier_buta_desen(int 가로, int Verticală_poziție, int 폭, int lungime_VALUE);
void Avizier_sfârșit_desen(void);
void Avizier_dreptunghi_umple(int 가로, int Verticală_poziție, int 폭, int lungime_VALUE, uint32_t 색);
/* real_date afișa_VALUE 메모리에 기록한 element_imagine 수. cursor 갱신은 제외한다. */
uint64_t Avizier_desen_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Verticală_poziție);
#endif
