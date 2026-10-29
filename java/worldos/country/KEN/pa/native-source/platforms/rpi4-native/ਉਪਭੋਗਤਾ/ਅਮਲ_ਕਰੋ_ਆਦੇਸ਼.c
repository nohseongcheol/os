#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼(int);
int ਉਪਭੋਗਤਾ_ਸੁਰੂ(int 전달값) {
    for (초기화함수 *ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ = __init_array_start; ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ < __init_array_end; ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ++) (*ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ)();
    int ਮਾਪ = ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼(전달값);
    for (초기화함수 *ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ = __fini_array_end; ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ != __fini_array_start;) (*--ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ)();
    return ਮਾਪ;
}
void *memset(void *ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ, int ਕੀਮਤ, size_t 항목수) { unsigned char *ਮੰਜਿਲ_ਸਮੱਗਰੀ = ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ; while (항목수--) *ਮੰਜਿਲ_ਸਮੱਗਰੀ++ = ਕੀਮਤ; return ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ; }
void *memcpy(void *ਮੰਜਿਲ_ਸਮੱਗਰੀ, const void *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ, size_t 항목수) { unsigned char *첫째값 = ਮੰਜਿਲ_ਸਮੱਗਰੀ; const unsigned char *둘째값 = ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ; while (항목수--) *첫째값++ = *둘째값++; return ਮੰਜਿਲ_ਸਮੱਗਰੀ; }
