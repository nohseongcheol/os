#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_кулланучы_кушымта(int);
int кулланучы_Start(int 전달값) {
    for (초기화함수 *мәгълүмат_урнаштыру = __init_array_start; мәгълүмат_урнаштыру < __init_array_end; мәгълүмат_урнаштыру++) (*мәгълүмат_урнаштыру)();
    int үлчәм = Start_кулланучы_кушымта(전달값);
    for (초기화함수 *мәгълүмат_урнаштыру = __fini_array_end; мәгълүмат_урнаштыру != __fini_array_start;) (*--мәгълүмат_урнаштыру)();
    return үлчәм;
}
void *memset(void *мәгълүмат_урнаштыру, int VALUE, size_t кертү_COUNT) { unsigned char *күчерү_урыны_мәгълүмат = мәгълүмат_урнаштыру; while (кертү_COUNT--) *күчерү_урыны_мәгълүмат++ = VALUE; return мәгълүмат_урнаштыру; }
void *memcpy(void *күчерү_урыны_мәгълүмат, const void *юл_мәгълүмат, size_t кертү_COUNT) { unsigned char *첫째값 = күчерү_урыны_мәгълүмат; const unsigned char *SECOND_VALUE = юл_мәгълүмат; while (кертү_COUNT--) *첫째값++ = *SECOND_VALUE++; return күчерү_урыны_мәгълүмат; }
