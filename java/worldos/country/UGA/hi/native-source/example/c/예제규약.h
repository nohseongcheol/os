#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int पाठ_की_बाइट_लंबाई(const char *पाठ) { int 길이=0;while(पाठ[길이])길이++;return 길이; }
static int निर्गम(const char *पाठ) { int 길이=पाठ_की_बाइट_लंबाई(पाठ);return लिखना_फ़ाइल_डेटा(1,पाठ,길이)==길이?0:1; }
#endif
