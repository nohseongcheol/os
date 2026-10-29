#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define کاربر_عکس_پایان_دادن 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define کاربر_پشته_آدرس 0x02f00000ul
#define کاربر_پایان_دادن 0x03000000ul
#define 사용자쪽수 ((کاربر_پایان_دادن - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define کاربر_داده_ها_خطا (-1001)
#define 사용자실행오류 (-1002)
#define کاربر_بی_اعتبار_دستورالعمل (-1003)
#define کاربر_پایان_مهلت_زمانی (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ثبت_نام_داده_ها[31], فرمان_مرتب_کردن, وضعیت_کد, پشته_آدرس; } کاربر_قاب;
void 사용자체계준비(void);
int کاربر_استثنا(کاربر_قاب *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t تخته_ای_کاربر_اجرا(uintptr_t);
uintptr_t تخته_ای_کاربر_ارزیابی_کردن(void);
uintptr_t تخته_ای_کنترل_کاربر(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
