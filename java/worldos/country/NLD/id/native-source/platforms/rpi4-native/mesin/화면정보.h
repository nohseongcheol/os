#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 aktual_data RGB32 화면 Ukuran. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Tersembunyi_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Papan_pointer(int 가로, int Vertikal_posisi, unsigned bentuk_VALUE);
/* 한 번에 32줄을 완성한 BACK_VALUE, 달라진 화소만 aktual_data 화면에 옮긴다. */
void Papan_Siapkan_gambar(volatile uint32_t *data, unsigned 폭, unsigned panjang_VALUE, unsigned spasi_baris_VALUE);
int 보드그림범위(int *가로, int *Vertikal_posisi, int *폭, int *panjang_VALUE);
int Papan_Mulai_gambar(int 가로, int Vertikal_posisi, int 폭, int panjang_VALUE);
void Papan_Selesai_gambar(void);
void Papan_persegi_isi(int 가로, int Vertikal_posisi, int 폭, int panjang_VALUE, uint32_t 색);
/* aktual_data show_VALUE 메모리에 기록한 elgam 수. pointer 갱신은 제외한다. */
uint64_t Papan_gambar_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikal_posisi);
#endif
