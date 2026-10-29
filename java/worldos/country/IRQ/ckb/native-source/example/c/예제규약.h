#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int دەق_درێژی(const char *دەق) { int درێژی_نرخ=0;while(دەق[درێژی_نرخ])درێژی_نرخ++;return درێژی_نرخ; }
static int 출력(const char *دەق) { int درێژی_نرخ=دەق_درێژی(دەق);return ڕایت_کردن_فایل_دەیتا(1,دەق,درێژی_نرخ)==درێژی_نرخ?0:1; }
#endif
