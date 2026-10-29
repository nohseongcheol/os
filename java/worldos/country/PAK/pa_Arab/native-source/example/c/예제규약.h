#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int متن_لمبائی(const char *متن) { int لمبائی_قدر=0;while(متن[لمبائی_قدر])لمبائی_قدر++;return لمبائی_قدر; }
static int 출력(const char *متن) { int لمبائی_قدر=متن_لمبائی(متن);return لکھو_فائل_کوائف(1,متن,لمبائی_قدر)==لمبائی_قدر?0:1; }
#endif
