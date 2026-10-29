#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void ਤਿਆਰ_ਕਰੋ_ਰਿਮੋਟ(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t ਬੋਰਡ_ਰਿਮੋਟ_ਨਿਯੰਤਰਣ(uintptr_t,uintptr_t);
uintptr_t ਬੋਰਡ_ਅੰਤ_ਰਿਮੋਟ_ਆਦੇਸ਼(uintptr_t);
uintptr_t 보드원격대기(uintptr_t);
void 원격화면살피기(void);
int ਨਿਯੰਤਰਣ_ਰਿਮੋਟ_ਪ੍ਰਦਰਸ਼ਨ(unsigned);
#endif
