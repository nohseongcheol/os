#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int متن_لمبائي(const char *متن) { int لمبائي_قدر=0;while(متن[لمبائي_قدر])لمبائي_قدر++;return لمبائي_قدر; }
static int 출력(const char *متن) { int لمبائي_قدر=متن_لمبائي(متن);return لکو_فائل_ڪوائف(1,متن,لمبائي_قدر)==لمبائي_قدر?0:1; }
#endif
