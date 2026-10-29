#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int පෙළ_දිග(const char *පෙළ) { int දිග_අගය=0;while(පෙළ[දිග_අගය])දිග_අගය++;return දිග_අගය; }
static int 출력(const char *පෙළ) { int දිග_අගය=පෙළ_දිග(පෙළ);return ලියන්න_ගොනුව_දත්ත(1,පෙළ,දිග_අගය)==දිග_අගය?0:1; }
#endif
