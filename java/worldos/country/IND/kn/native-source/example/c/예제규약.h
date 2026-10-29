#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int ಪಠ್ಯ_ಉದ್ದ(const char *ಪಠ್ಯ) { int ಉದ್ದ_ಮೌಲ್ಯ=0;while(ಪಠ್ಯ[ಉದ್ದ_ಮೌಲ್ಯ])ಉದ್ದ_ಮೌಲ್ಯ++;return ಉದ್ದ_ಮೌಲ್ಯ; }
static int ಔಟ್_ಪುಟ್(const char *ಪಠ್ಯ) { int ಉದ್ದ_ಮೌಲ್ಯ=ಪಠ್ಯ_ಉದ್ದ(ಪಠ್ಯ);return ಬರೆ_ಫೈಲ್_ಡೇಟಾ(1,ಪಠ್ಯ,ಉದ್ದ_ಮೌಲ್ಯ)==ಉದ್ದ_ಮೌಲ್ಯ?0:1; }
#endif
