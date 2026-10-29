#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 fiili_veri RGB32 화면 Boyut. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Gizli_değer, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Pano_işaretçi(int 가로, int Dikey_konum, unsigned şekil_değer);
/* 한 번에 32줄을 완성한 BACK_değer, 달라진 화소만 fiili_veri 화면에 옮긴다. */
void Pano_Hazırlan_çizim(volatile uint32_t *veri, unsigned 폭, unsigned süre_değer, unsigned satır_aralığı_değer);
int 보드그림범위(int *가로, int *Dikey_konum, int *폭, int *süre_değer);
int Pano_Start_çizim(int 가로, int Dikey_konum, int 폭, int süre_değer);
void Pano_Son_çizim(void);
void Pano_dikdörtgen_dolgu(int 가로, int Dikey_konum, int 폭, int süre_değer, uint32_t 색);
/* fiili_veri şov_değer 메모리에 기록한 piksel 수. işaretçi 갱신은 제외한다. */
uint64_t Pano_çizim_BAĞ_DEĞ_SAY(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Dikey_konum);
#endif
