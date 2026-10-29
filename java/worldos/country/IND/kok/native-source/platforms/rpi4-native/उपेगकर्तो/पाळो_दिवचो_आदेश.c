#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_उपेगकर्तो_एप्लिकेशन(int);
int उपेगकर्तो_Start(int 전달값) {
    for (초기화함수 *डेटा_स्थिती = __init_array_start; डेटा_स्थिती < __init_array_end; डेटा_स्थिती++) (*डेटा_स्थिती)();
    int मेजप = Start_उपेगकर्तो_एप्लिकेशन(전달값);
    for (초기화함수 *डेटा_स्थिती = __fini_array_end; डेटा_स्थिती != __fini_array_start;) (*--डेटा_स्थिती)();
    return मेजप;
}
void *memset(void *डेटा_स्थिती, int मोल, size_t प्रवेश_COUNT) { unsigned char *नियुक्त_स्थान_डेटा = डेटा_स्थिती; while (प्रवेश_COUNT--) *नियुक्त_स्थान_डेटा++ = मोल; return डेटा_स्थिती; }
void *memcpy(void *नियुक्त_स्थान_डेटा, const void *स्ट्रिंग_डेटा, size_t प्रवेश_COUNT) { unsigned char *첫째값 = नियुक्त_स्थान_डेटा; const unsigned char *SECOND_मोल = स्ट्रिंग_डेटा; while (प्रवेश_COUNT--) *첫째값++ = *SECOND_मोल++; return नियुक्त_स्थान_डेटा; }
