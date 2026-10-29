#include "../명명/စက်ချိတ်အမည်များ.h"
#include "ခေါ်လုပ်.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int သုံးစွဲသူပရိုဂရမ်စတင်(int);
int သုံးစွဲသူစတင်(int 전달값) {
    for (초기화함수 *ဒေတာနေရာ = __init_array_start; ဒေတာနေရာ < __init_array_end; ဒေတာနေရာ++) (*ဒေတာနေရာ)();
    int ရလဒ် = သုံးစွဲသူပရိုဂရမ်စတင်(전달값);
    for (초기화함수 *ဒေတာနေရာ = __fini_array_end; ဒေတာနေရာ != __fini_array_start;) (*--ဒေတာနေရာ)();
    return ရလဒ်;
}
void *memset(void *ဒေတာနေရာ, int တန်ဖိုး, size_t အချက်အရေအတွက်) { unsigned char *ဦးတည်ရာဒေတာ = ဒေတာနေရာ; while (အချက်အရေအတွက်--) *ဦးတည်ရာဒေတာ++ = တန်ဖိုး; return ဒေတာနေရာ; }
void *memcpy(void *ဦးတည်ရာဒေတာ, const void *အက္ခရာစဉ်ဒေတာ, size_t အချက်အရေအတွက်) { unsigned char *ပထမတန်ဖိုး = ဦးတည်ရာဒေတာ; const unsigned char *ဒုတိယတန်ဖိုး = အက္ခရာစဉ်ဒေတာ; while (အချက်အရေအတွက်--) *ပထမတန်ဖိုး++ = *ဒုတိယတန်ဖိုး++; return ဦးတည်ရာဒေတာ; }
