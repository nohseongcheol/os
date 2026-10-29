#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_urefu(const char *SMS) { int urefu_thamani=0;while(SMS[urefu_thamani])urefu_thamani++;return urefu_thamani; }
static int 출력(const char *SMS) { int urefu_thamani=SMS_urefu(SMS);return andika_faili_data(1,SMS,urefu_thamani)==urefu_thamani?0:1; }
#endif
