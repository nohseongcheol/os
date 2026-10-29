#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int पाठ_लम्बाइ(const char *पाठ) { int लम्बाइ_मान=0;while(पाठ[लम्बाइ_मान])लम्बाइ_मान++;return लम्बाइ_मान; }
static int 출력(const char *पाठ) { int लम्बाइ_मान=पाठ_लम्बाइ(पाठ);return लेख्नुहोस्_फाइल_लगत(1,पाठ,लम्बाइ_मान)==लम्बाइ_मान?0:1; }
#endif
