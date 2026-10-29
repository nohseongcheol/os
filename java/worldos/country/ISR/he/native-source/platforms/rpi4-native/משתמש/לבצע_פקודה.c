#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int התחל_משתמש_תוכנית(int);
int משתמש_התחל(int 전달값) {
    for (초기화함수 *נתונים_עמדה = __init_array_start; נתונים_עמדה < __init_array_end; נתונים_עמדה++) (*נתונים_עמדה)();
    int תוצאה = התחל_משתמש_תוכנית(전달값);
    for (초기화함수 *נתונים_עמדה = __fini_array_end; נתונים_עמדה != __fini_array_start;) (*--נתונים_עמדה)();
    return תוצאה;
}
void *memset(void *נתונים_עמדה, int ערך, size_t 항목수) { unsigned char *יעד_נתונים = נתונים_עמדה; while (항목수--) *יעד_נתונים++ = ערך; return נתונים_עמדה; }
void *memcpy(void *יעד_נתונים, const void *מחרוזת_נתונים, size_t 항목수) { unsigned char *첫째값 = יעד_נתונים; const unsigned char *둘째값 = מחרוזת_נתונים; while (항목수--) *첫째값++ = *둘째값++; return יעד_נתונים; }
