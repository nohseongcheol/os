#ifndef ดั้งเดิม_การเข้ารหัส_ส่วนหัว
#define ดั้งเดิม_การเข้ารหัส_ส่วนหัว
#include <stddef.h>
#include <stdint.h>
void *จัดสรร_ระยะไกล(size_t);
void ปล่อย_ระยะไกล(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void ระยะไกล_สรุป(const void *, size_t, unsigned char [32]);
#endif
