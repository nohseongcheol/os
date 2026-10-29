#ifndef ดั้งเดิม_ผู้ใช้_โทร_ส่วนหัว
#define ดั้งเดิม_ผู้ใช้_โทร_ส่วนหัว
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 ดัชนี, x0..x5=อาร์กิวเมนต์, x0=ผลลัพธ์/음수 ข้อผิดพลาด. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t ดัชนี, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t ทะเบียน_ศูนย์ __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = ดัชนี;
    __asm__ volatile("svc #0" : "+r"(ทะเบียน_ศูนย์) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)ทะเบียน_ศูนย์;
}
static inline intptr_t 화면사각형(unsigned พิกัดแกน_x, unsigned 세로좌표, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, พิกัดแกน_x, 세로좌표, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t ผู้ใช้_ความจํา_สิ้นสุดการโทร(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t ผลลัพธ์ = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (ผลลัพธ์ < 0) return ผลลัพธ์;
    do { ผลลัพธ์ = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (ผลลัพธ์ == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return ผลลัพธ์;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t ผู้ใช้_อาร์กิวเมนต์(unsigned ดัชนี, char *เนื้อหา_ค่า, size_t ขนาด) {
    return 사용자호출(15, ดัชนี, (uintptr_t)เนื้อหา_ค่า, ขนาด, 0, 0, 0);
}
#endif
