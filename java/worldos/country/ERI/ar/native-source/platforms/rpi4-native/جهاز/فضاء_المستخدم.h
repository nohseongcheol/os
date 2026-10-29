#ifndef أصلي_مستخدم_عنوان
#define أصلي_مستخدم_عنوان
#include <stdint.h>
#include <stddef.h>
#define مستخدم_أساس 0x02000000ul
#define مستخدم_صورة_إنهاء_مكالمة 0x02c00000ul
#define مستخدم_كومة_ذاكرة_مؤقتة_إنهاء_مكالمة 0x02ed0000ul
#define مستخدم_رمز_عنوان 0x02f00000ul
#define مستخدم_إنهاء_مكالمة 0x03000000ul
#define 사용자쪽수 ((مستخدم_إنهاء_مكالمة - مستخدم_أساس) / 4096ul)
#define 사용자실행파일오류 (-8)
#define مستخدم_بيانات_خطأ (-1001)
#define 사용자실행오류 (-1002)
#define مستخدم_غير_صالح_تعليمة (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t سجل_بيانات[31], أمر_منصب, حالة_رمز, رمز_عنوان; } مستخدم_شكل;
void 사용자체계준비(void);
int استثناء_المستخدم(مستخدم_شكل *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t لوحة_مستخدم_يشغّل(uintptr_t);
uintptr_t لوحة_مستخدم_التحقق_من_صحة(void);
uintptr_t لوحة_عنصر_تحكم_للمستخدم(uintptr_t);
uint32_t يقرأ_مستخدم_حالة(unsigned, unsigned);
#endif
