#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int เริ่ม_ผู้ใช้_แอป(int);
int ผู้ใช้_เริ่ม(int 전달값) {
    for (초기화함수 *ข้อมูล_ตําแหน่ง = __init_array_start; ข้อมูล_ตําแหน่ง < __init_array_end; ข้อมูล_ตําแหน่ง++) (*ข้อมูล_ตําแหน่ง)();
    int ผลลัพธ์ = เริ่ม_ผู้ใช้_แอป(전달값);
    for (초기화함수 *ข้อมูล_ตําแหน่ง = __fini_array_end; ข้อมูล_ตําแหน่ง != __fini_array_start;) (*--ข้อมูล_ตําแหน่ง)();
    return ผลลัพธ์;
}
void *memset(void *ข้อมูล_ตําแหน่ง, int ค่า, size_t 항목수) { unsigned char *ปลายทาง_ข้อมูล = ข้อมูล_ตําแหน่ง; while (항목수--) *ปลายทาง_ข้อมูล++ = ค่า; return ข้อมูล_ตําแหน่ง; }
void *memcpy(void *ปลายทาง_ข้อมูล, const void *สตริง_ข้อมูล, size_t 항목수) { unsigned char *첫째값 = ปลายทาง_ข้อมูล; const unsigned char *둘째값 = สตริง_ข้อมูล; while (항목수--) *첫째값++ = *둘째값++; return ปลายทาง_ข้อมูล; }
