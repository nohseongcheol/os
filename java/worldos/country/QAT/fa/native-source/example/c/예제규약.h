#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int متن_طول(const char *متن) { int طول_مقدار=0;while(متن[طول_مقدار])طول_مقدار++;return طول_مقدار; }
static int خروجی(const char *متن) { int طول_مقدار=متن_طول(متن);return نوشتن_فایل_داده_ها(1,متن,طول_مقدار)==طول_مقدار?0:1; }
#endif
