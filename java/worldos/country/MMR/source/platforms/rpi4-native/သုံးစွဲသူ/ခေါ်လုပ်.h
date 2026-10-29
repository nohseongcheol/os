#ifndef ကိုယ်ပိုင်သုံးစွဲသူခေါ်ခေါင်းစီး
#define ကိုယ်ပိုင်သုံးစွဲသူခေါ်ခေါင်းစီး
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=ခေါ်လုပ် နံပါတ်, x0..x5=အချက်များ, x0=ရလဒ်/အနုတ်တန်ဖိုး အမှား. Linux ABI 아님.
static inline intptr_t သုံးစွဲသူခေါ်လုပ်(uintptr_t နံပါတ်, uintptr_t ပထမတွက်ချက်ခံ, uintptr_t ဒုတိယတွက်ချက်ခံ, uintptr_t တတိယအော်ပရန်း,
                                uintptr_t စတုတ္ထအော်ပရန်း, uintptr_t ပဉ္စမအော်ပရန်း, uintptr_t 바) {
    register uintptr_t သုညအမြန်မှတ်ကွက် __asm__("x0") = ပထမတွက်ချက်ခံ;
    register uintptr_t 저장기일 __asm__("x1") = ဒုတိယတွက်ချက်ခံ;
    register uintptr_t 저장기이 __asm__("x2") = တတိယအော်ပရန်း;
    register uintptr_t 저장기삼 __asm__("x3") = စတုတ္ထအော်ပရန်း;
    register uintptr_t 저장기사 __asm__("x4") = ပဉ္စမအော်ပရန်း;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = နံပါတ်;
    __asm__ volatile("svc #0" : "+r"(သုညအမြန်မှတ်ကွက်) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)သုညအမြန်မှတ်ကွက်;
}
static inline intptr_t မျက်နှာပြင်စတုဂံ(unsigned xတည်နေရာအမှတ်, unsigned yတည်နေရာအမှတ်, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return သုံးစွဲသူခေါ်လုပ်(13, xတည်နေရာအမှတ်, yတည်နေရာအမှတ်, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t သုံးစွဲသူမှတ်ဉာဏ်အဆုံး(uintptr_t အဆုံး) { return သုံးစွဲသူခေါ်လုပ်(8, အဆုံး, 0, 0, 0, 0, 0); }
static inline intptr_t မျက်နှာပြင်အနံဖတ်(void) { return သုံးစွဲသူခေါ်လုပ်(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t မျက်နှာပြင်အမြင့်ဖတ်(void) { return သုံးစွဲသူခေါ်လုပ်(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t ရလဒ် = သုံးစွဲသူခေါ်လုပ်(16, 0, 0, 0, 0, 0, 0);
    if (ရလဒ် < 0) return ရလဒ်;
    do { ရလဒ် = သုံးစွဲသူခေါ်လုပ်(16, 1, 0, 0, 0, 0, 0); } while (ရလဒ် == -11);
    သုံးစွဲသူခေါ်လုပ်(16, 2, 0, 0, 0, 0, 0);
    return ရလဒ်;
}
static inline intptr_t သုံးစွဲသူပေးအချက်အရေအတွက်(void) { return သုံးစွဲသူခေါ်လုပ်(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t သုံးစွဲသူပေးအချက်(unsigned နံပါတ်, char *အကြောင်းအရာတန်ဖိုး, size_t အရွယ်) {
    return သုံးစွဲသူခေါ်လုပ်(15, နံပါတ်, (uintptr_t)အကြောင်းအရာတန်ဖိုး, အရွယ်, 0, 0, 0);
}
#endif
