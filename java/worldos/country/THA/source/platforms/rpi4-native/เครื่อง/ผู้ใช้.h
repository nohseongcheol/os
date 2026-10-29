#ifndef ดั้งเดิม_ผู้ใช้_ส่วนหัว
#define ดั้งเดิม_ผู้ใช้_ส่วนหัว
#include <stdint.h>
#include <stddef.h>
#define ผู้ใช้_ฐาน 0x02000000ul
#define ผู้ใช้_รูป_สิ้นสุดการโทร 0x02c00000ul
#define ผู้ใช้_ฮีป_สิ้นสุดการโทร 0x02ed0000ul
#define ผู้ใช้_สแตก_อีเมล 0x02f00000ul
#define ผู้ใช้_สิ้นสุดการโทร 0x03000000ul
#define 사용자쪽수 ((ผู้ใช้_สิ้นสุดการโทร - ผู้ใช้_ฐาน) / 4096ul)
#define ผู้ใช้_แฟ้มปฏิบัติการ_ข้อผิดพลาด (-8)
#define ผู้ใช้_ข้อมูล_ข้อผิดพลาด (-1001)
#define 사용자실행오류 (-1002)
#define 사용자잘못된명령 (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ทะเบียน_ข้อมูล[31], คําสั่ง_ตําแหน่ง, สถานะ_รหัส, สแตก_อีเมล; } ผู้ใช้_กรอบ;
void 사용자체계준비(void);
int ข้อผิดพลาดขณะใช้งาน(ผู้ใช้_กรอบ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t บอร์ด_ผู้ใช้_ใช้งาน(uintptr_t);
uintptr_t บอร์ด_ผู้ใช้_ตรวจสอบความถูกต้อง(void);
uintptr_t บอร์ด_ตัวควบคุมของผู้ใช้(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
