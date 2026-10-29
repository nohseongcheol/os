#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ສະຕຣິງ_ຄ່າ);
int strcmp(const char *ດ້ານຫນ້າ_ຄ່າ, const char *ກັບ_ຄືນ_ຄ່າ);
int memcmp(const void *ດ້ານຫນ້າ_ຄ່າ, const void *ກັບ_ຄືນ_ຄ່າ, size_t 바이트수);
void *memcpy(void *ປາຍທາງ_ຄ່າ, const void *원본, size_t 바이트수);
void *memset(void *ປາຍທາງ_ຄ່າ, int ຄ່າ, size_t 바이트수);
#endif
