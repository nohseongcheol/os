#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Testenn) { int 길이=0;while(Testenn[길이])길이++;return 길이; }
static int Ec_hankad(const char *Testenn) { int 길이=글길이(Testenn);return 파일자료쓰기(1,Testenn,길이)==길이?0:1; }
#endif
