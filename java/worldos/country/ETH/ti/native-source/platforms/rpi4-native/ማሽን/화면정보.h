#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 ትኽክለኛ_ሓበሬታ RGB32 화면 መጠን. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: ሕቡእ_ዋጋ, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 보드포인터(int 가로, int 세로, unsigned ቅርጺ_ዋጋ);
/* 한 번에 32줄을 완성한 ድሕሪት_ዋጋ, 달라진 화소만 ትኽክለኛ_ሓበሬታ 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *ሓበሬታ, unsigned 폭, unsigned ንውሓት_ዋጋ, unsigned መራሒ_ዋጋ);
int 보드그림범위(int *가로, int *세로, int *폭, int *ንውሓት_ዋጋ);
int 보드그림시작(int 가로, int 세로, int 폭, int ንውሓት_ዋጋ);
void 보드그림마침(void);
void 보드사각그림(int 가로, int 세로, int 폭, int ንውሓት_ዋጋ, uint32_t 색);
/* ትኽክለኛ_ሓበሬታ ኣርእይ_ዋጋ 메모리에 기록한 ንጣብ 수. ኣመልካቲ 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned 세로);
#endif
