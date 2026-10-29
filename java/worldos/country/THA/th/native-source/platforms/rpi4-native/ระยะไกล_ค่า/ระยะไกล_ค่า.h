#ifndef ดั้งเดิม_การเชื่อมต่อระยะไกล_ส่วนหัว
#define ดั้งเดิม_การเชื่อมต่อระยะไกล_ส่วนหัว
#include "../명명/기계연결이름.h"
#include <stdint.h>
void จัดเตรียม_ระยะไกล(void);
void 원격살피기(void);
void ระยะไกล_ผลผลิต(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t บอร์ด_การควบคุมระยะไกล(uintptr_t,uintptr_t);
uintptr_t บอร์ด_สิ้นสุดการโทร_ระยะไกล_คําสั่ง(uintptr_t);
uintptr_t บอร์ด_ระยะไกล_รอเดี๋ยว(uintptr_t);
void 원격화면살피기(void);
int ควบคุม_ระยะไกล_แสดง(unsigned);
#endif
