#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define صارف_نقش_اختتام 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define صارف_اسٹیک_پتہ 0x02f00000ul
#define صارف_اختتام 0x03000000ul
#define 사용자쪽수 ((صارف_اختتام - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define صارف_کوائف_نقص (-1001)
#define 사용자실행오류 (-1002)
#define صارف_بے_جواز_ہدایت (-1003)
#define صارف_ٹائم_آؤٹ (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t رجسٹر_کریں_کوائف[31], حکم_پوزیشن_ٹھیک_کریں, 상태값, اسٹیک_پتہ; } صارف_فریم;
void 사용자체계준비(void);
int صارف_استثنا(صارف_فریم *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t بورڈ_صارف_چلائیں(uintptr_t);
uintptr_t بورڈ_صارف_جواز_دہی_کریں(void);
uintptr_t بورڈ_صارف_کنٹرول(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
