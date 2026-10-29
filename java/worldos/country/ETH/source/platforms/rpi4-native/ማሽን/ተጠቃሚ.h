#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ተጠቃሚ_ምስል_ጨርስ 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ተጠቃሚ_ክምር_አድራሻ 0x02f00000ul
#define ተጠቃሚ_ጨርስ 0x03000000ul
#define 사용자쪽수 ((ተጠቃሚ_ጨርስ - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ተጠቃሚ_ውሂብ_ስህተት (-1001)
#define 사용자실행오류 (-1002)
#define ተጠቃሚ_ልክ_ያልኾነ_መምሪያ (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t መዝግብ_ውሂብ[31], ትእዛዝ_በቦታ_አስቀመጠ, 상태값, ክምር_አድራሻ; } ተጠቃሚ_ማዕቀፍ;
void 사용자체계준비(void);
int ተጠቃሚ_ልዩነት(ተጠቃሚ_ማዕቀፍ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ቦርድ_ተጠቃሚ_አሂድ(uintptr_t);
uintptr_t ቦርድ_ተጠቃሚ_ትክክለኛነት_አረጋግጥ(void);
uintptr_t ቦርድ_የተጠቃሚ_ቁጥጥር(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
