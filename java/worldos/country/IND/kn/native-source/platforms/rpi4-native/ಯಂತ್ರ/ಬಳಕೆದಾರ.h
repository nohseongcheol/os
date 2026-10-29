#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ಬಳಕೆದಾರ_ಇಮೇಜ್_ಅಂತ್ಯಗೊಳಿಸು 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ಬಳಕೆದಾರ_ಸ್ಟ್ಯಾಕ್_ಇಮೇಲ್ 0x02f00000ul
#define ಬಳಕೆದಾರ_ಅಂತ್ಯಗೊಳಿಸು 0x03000000ul
#define 사용자쪽수 ((ಬಳಕೆದಾರ_ಅಂತ್ಯಗೊಳಿಸು - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ಬಳಕೆದಾರ_ಡೇಟಾ_ದೋಷ (-1001)
#define 사용자실행오류 (-1002)
#define ಬಳಕೆದಾರ_ಅಮಾನ್ಯ_ಸೂಚನೆ (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ನೋಂದಾಯಿಸು_ಡೇಟಾ[31], ಆದೇಶ_ಹುದ್ದೆ, ಸ್ಥಿತಿ_ಕೋಡ್, ಸ್ಟ್ಯಾಕ್_ಇಮೇಲ್; } ಬಳಕೆದಾರ_ಫ್ರೇಮ್;
void 사용자체계준비(void);
int ಬಳಕೆದಾರ_ವಿನಾಯಿತಿ(ಬಳಕೆದಾರ_ಫ್ರೇಮ್ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ಬೋರ್ಡ್_ಬಳಕೆದಾರ_ಚಲನೆ(uintptr_t);
uintptr_t ಬೋರ್ಡ್_ಬಳಕೆದಾರ_ಸಕ್ರಮೀಕರಿಸು(void);
uintptr_t ಬೋರ್ಡ್_ಬಳಕೆದಾರ_ನಿಯಂತ್ರಣ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
