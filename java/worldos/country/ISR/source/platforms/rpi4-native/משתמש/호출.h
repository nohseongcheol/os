#ifndef מקורי_משתמש_שיחה_כותרת
#define מקורי_משתמש_שיחה_כותרת
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 מדד, x0..x5=ארגומנטים, x0=תוצאה/음수 שגיאה. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t מדד, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t אוגר_אפס __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = מדד;
    __asm__ volatile("svc #0" : "+r"(אוגר_אפס) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)אוגר_אפס;
}
static inline intptr_t 화면사각형(unsigned קואורדינטת_x, unsigned 세로좌표, unsigned 너비값, unsigned נדרש_גובה_ערך, unsigned 빛삼원색) {
    return 사용자호출(13, קואורדינטת_x, 세로좌표, 빛삼원색, 너비값, נדרש_גובה_ערך, 0);
}
static inline intptr_t משתמש_זיכרון_סיים_שיחה(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t תוצאה = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (תוצאה < 0) return תוצאה;
    do { תוצאה = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (תוצאה == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return תוצאה;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t משתמש_ארגומנט(unsigned מדד, char *תוכן_ערך, size_t גודל) {
    return 사용자호출(15, מדד, (uintptr_t)תוכן_ערך, גודל, 0, 0, 0);
}
#endif
