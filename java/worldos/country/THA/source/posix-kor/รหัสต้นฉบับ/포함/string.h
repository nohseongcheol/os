#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *สตริง_ค่า);
int strcmp(const char *กล้องหน้า_ค่า, const char *ย้อนกลับ_ค่า);
int memcmp(const void *กล้องหน้า_ค่า, const void *ย้อนกลับ_ค่า, size_t 바이트수);
void *memcpy(void *ปลายทาง_ค่า_a0fbc067, const void *원본, size_t 바이트수);
void *memset(void *ปลายทาง_ค่า_a0fbc067, int ค่า, size_t 바이트수);
#endif
