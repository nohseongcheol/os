#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 ትክክለኛ_ውሂብ RGB32 화면 መጠን. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: ድብቅ_እሴት, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void ቦርድ_ጠቋሚ(int 가로, int ቋሚ_በቦታ_አስቀመጠ, unsigned ቅርጽ_እሴት);
/* 한 번에 32줄을 완성한 ተመለስ_እሴት, 달라진 화소만 ትክክለኛ_ውሂብ 화면에 옮긴다. */
void ቦርድ_አዘጋጅ_ስዕል(volatile uint32_t *ውሂብ, unsigned 폭, unsigned ርዝመት_እሴት, unsigned መሪ_እሴት);
int 보드그림범위(int *가로, int *ቋሚ_በቦታ_አስቀመጠ, int *폭, int *ርዝመት_እሴት);
int ቦርድ_ጀምር_ስዕል(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int ርዝመት_እሴት);
void ቦርድ_ጨርስ_ስዕል(void);
void 보드사각그림(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int ርዝመት_እሴት, uint32_t 색);
/* ትክክለኛ_ውሂብ አሳይ_እሴት 메모리에 기록한 ፒክስል 수. ጠቋሚ 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned ቋሚ_በቦታ_አስቀመጠ);
#endif
