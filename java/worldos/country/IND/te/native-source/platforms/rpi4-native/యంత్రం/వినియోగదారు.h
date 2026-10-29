#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define వినియోగదారు_చిత్రం_ముగించు 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define వినియోగదారు_దొంతర_ఇమెయిల్ 0x02f00000ul
#define వినియోగదారు_ముగించు 0x03000000ul
#define 사용자쪽수 ((వినియోగదారు_ముగించు - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define వినియోగదారు_డేటా_దోషం (-1001)
#define 사용자실행오류 (-1002)
#define వినియోగదారు_చెల్లని_సూచన (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t నమోదు_చేయి_డేటా[31], ఆదేశం_స్థాయి, స్థితి_కోడ్, దొంతర_ఇమెయిల్; } వినియోగదారు_చట్రం;
void 사용자체계준비(void);
int వినియోగదారు_మినహాయింపు(వినియోగదారు_చట్రం *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t బోర్డు_వినియోగదారు_అమలు_చెయ్(uintptr_t);
uintptr_t బోర్డు_వినియోగదారు_నిర్థారీకరించు(void);
uintptr_t బోర్డు_వినియోగదారు_నియంత్రణ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
