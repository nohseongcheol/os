#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_लांबाय(const char *SMS) { int लांबाय_मोल=0;while(SMS[लांबाय_मोल])लांबाय_मोल++;return लांबाय_मोल; }
static int 출력(const char *SMS) { int लांबाय_मोल=SMS_लांबाय(SMS);return बरोवचें_फायल_डेटा(1,SMS,लांबाय_मोल)==लांबाय_मोल?0:1; }
#endif
