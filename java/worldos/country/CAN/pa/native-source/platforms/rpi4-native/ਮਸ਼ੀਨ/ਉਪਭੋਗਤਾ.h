#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ਉਪਭੋਗਤਾ_ਤਸਵੀਰ_ਅੰਤ 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ਉਪਭੋਗਤਾ_ਸਟੈਕ_ਪਤਾ 0x02f00000ul
#define ਉਪਭੋਗਤਾ_ਅੰਤ 0x03000000ul
#define 사용자쪽수 ((ਉਪਭੋਗਤਾ_ਅੰਤ - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ਉਪਭੋਗਤਾ_ਸਮੱਗਰੀ_ਗਲਤ (-1001)
#define 사용자실행오류 (-1002)
#define ਉਪਭੋਗਤਾ_ਅਯੋਗ_ਨਿਰਦੇਸ਼ (-1003)
#define ਉਪਭੋਗਤਾ_ਸਮਾਂ_ਸਮਾਪਤ (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ਰਜਿਸਟਰ_ਕਰੋ_ਸਮੱਗਰੀ[31], ਆਦੇਸ਼_ਸਥਿਤੀ_ਬਦਲੋ, 상태값, ਸਟੈਕ_ਪਤਾ; } ਉਪਭੋਗਤਾ_ਖਾਕਾ;
void 사용자체계준비(void);
int 사용자예외(ਉਪਭੋਗਤਾ_ਖਾਕਾ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ਬੋਰਡ_ਉਪਭੋਗਤਾ_ਚਲਾਉ(uintptr_t);
uintptr_t ਬੋਰਡ_ਉਪਭੋਗਤਾ_ਪ੍ਰਮਾਣਿਤ(void);
uintptr_t ਬੋਰਡ_ਉਪਭੋਗਤਾ_ਨਿਯੰਤਰਣ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
