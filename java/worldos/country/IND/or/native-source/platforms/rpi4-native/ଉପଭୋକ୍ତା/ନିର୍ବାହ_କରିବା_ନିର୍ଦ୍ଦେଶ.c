#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ(int);
int ଉପଭୋକ୍ତା_ଆରମ୍ଭ(int 전달값) {
    for (초기화함수 *ଡାଟା_ସ୍ଥିତି = __init_array_start; ଡାଟା_ସ୍ଥିତି < __init_array_end; ଡାଟା_ସ୍ଥିତି++) (*ଡାଟା_ସ୍ଥିତି)();
    int ମାପ = ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ(전달값);
    for (초기화함수 *ଡାଟା_ସ୍ଥିତି = __fini_array_end; ଡାଟା_ସ୍ଥିତି != __fini_array_start;) (*--ଡାଟା_ସ୍ଥିତି)();
    return ମାପ;
}
void *memset(void *ଡାଟା_ସ୍ଥିତି, int ମୂଲ୍ୟ, size_t 항목수) { unsigned char *ଲକ୍ଷସ୍ଥଳ_ଡାଟା = ଡାଟା_ସ୍ଥିତି; while (항목수--) *ଲକ୍ଷସ୍ଥଳ_ଡାଟା++ = ମୂଲ୍ୟ; return ଡାଟା_ସ୍ଥିତି; }
void *memcpy(void *ଲକ୍ଷସ୍ଥଳ_ଡାଟା, const void *ଷ୍ଟ୍ରିଂ_ଡାଟା, size_t 항목수) { unsigned char *첫째값 = ଲକ୍ଷସ୍ଥଳ_ଡାଟା; const unsigned char *둘째값 = ଷ୍ଟ୍ରିଂ_ଡାଟା; while (항목수--) *첫째값++ = *둘째값++; return ଲକ୍ଷସ୍ଥଳ_ଡାଟା; }
