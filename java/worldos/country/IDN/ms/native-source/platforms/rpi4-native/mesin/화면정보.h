#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 sebenar_data RGB32 화면 Saiz. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Tersembunyi_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Papan_penuding(int 가로, int Menegak_jawatan, unsigned bentuk_VALUE);
/* 한 번에 32줄을 완성한 BACK_VALUE, 달라진 화소만 sebenar_data 화면에 옮긴다. */
void Papan_Sediakan_lukisan(volatile uint32_t *data, unsigned 폭, unsigned kepanjangan_VALUE, unsigned jarak_baris_VALUE);
int 보드그림범위(int *가로, int *Menegak_jawatan, int *폭, int *kepanjangan_VALUE);
int Papan_Mula_lukisan(int 가로, int Menegak_jawatan, int 폭, int kepanjangan_VALUE);
void Papan_Tamat_lukisan(void);
void Papan_segi_empat_tepat_isi(int 가로, int Menegak_jawatan, int 폭, int kepanjangan_VALUE, uint32_t 색);
/* sebenar_data tayang_VALUE 메모리에 기록한 pel 수. penuding 갱신은 제외한다. */
uint64_t Papan_lukisan_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Menegak_jawatan);
#endif
