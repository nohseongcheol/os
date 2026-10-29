#ifndef ดั้งเดิม_เครือข่าย_ส่วนหัว
#define ดั้งเดิม_เครือข่าย_ส่วนหัว
#include <stdint.h>
#include <stddef.h>
void จัดเตรียม_เครือข่าย(void);
void 통신망살피기(void);
int 통신끝점만들기(int ชนิด_ประเภท);
int สุทธิ_ผูก(int แฟ้ม_จุดจับ, uint32_t อีเมล, unsigned หมายเลขพอร์ต);
int สุทธิ_รอการติดต่อ(int แฟ้ม_จุดจับ);
void 통신주소재사용(int แฟ้ม_จุดจับ);
int สุทธิ_เชื่อมต่อ(int แฟ้ม_จุดจับ, uint32_t อีเมล, unsigned หมายเลขพอร์ต);
int สุทธิ_ยอมรับ(int แฟ้ม_จุดจับ);
int 통신읽기(int แฟ้ม_จุดจับ, void *ข้อมูล, unsigned 개수);
int 통신쓰기(int แฟ้ม_จุดจับ, const void *ข้อมูล, unsigned 개수);
int ส่ง_เดตาแกรม(int แฟ้ม_จุดจับ, const void *ข้อมูล, unsigned 개수, uint32_t อีเมล, unsigned หมายเลขพอร์ต);
int รับ_เดตาแกรม(int แฟ้ม_จุดจับ, void *ข้อมูล, unsigned 개수);
unsigned เครือข่าย_หมายเลขพอร์ต(int แฟ้ม_จุดจับ);
unsigned ชั้น_หมายเลขพอร์ต(int แฟ้ม_จุดจับ);
uint32_t สุทธิ_ชั้น_อีเมล(int แฟ้ม_จุดจับ);
void ปิด_เครือข่าย(int แฟ้ม_จุดจับ);
int การถ่ายโอนแฟ้ม_ควบคุม(int การกระทํา);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned รายการ_ค่า, unsigned ดัชนี);
int กําหนดค่า_เครือข่าย(unsigned การกระทํา, uint32_t อีเมล, uint32_t มาสก์_ค่า, uint32_t เกตเวย์_ค่า);
int เริ่ม_การตอบ_การทดสอบ(uint32_t อีเมล, unsigned ลําดับ_ค่า);
int 응답시험읽기(unsigned รายการ_ค่า);
#endif
