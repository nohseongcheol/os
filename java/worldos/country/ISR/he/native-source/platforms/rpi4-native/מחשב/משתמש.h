#ifndef מקורי_משתמש_כותרת
#define מקורי_משתמש_כותרת
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define משתמש_תמונה_סיים_שיחה 0x02c00000ul
#define משתמש_ערימה_סיים_שיחה 0x02ed0000ul
#define משתמש_רמז_למען 0x02f00000ul
#define משתמש_סיים_שיחה 0x03000000ul
#define 사용자쪽수 ((משתמש_סיים_שיחה - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define משתמש_נתונים_שגיאה (-1001)
#define 사용자실행오류 (-1002)
#define משתמש_לא_חוקי_הוראה (-1003)
#define משתמש_פסק_זמן (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t אוגר_נתונים[31], פקודה_עמדה, מצב_קוד, רמז_למען; } משתמש_למסגר;
void 사용자체계준비(void);
int חריגת_משתמש(משתמש_למסגר *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t לוח_משתמש_להפעיל(uintptr_t);
uintptr_t לוח_משתמש_לאמת(void);
uintptr_t לוח_פקד_משתמש(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
