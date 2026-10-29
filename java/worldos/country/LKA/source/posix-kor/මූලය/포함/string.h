#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *අනුලකුණු_වැල_අගය);
int strcmp(const char *앞, const char *ආපසු_අගය);
int memcmp(const void *앞, const void *ආපසු_අගය, size_t 바이트수);
void *memcpy(void *ගමනාන්තය_අගය, const void *원본, size_t 바이트수);
void *memset(void *ගමනාන්තය_අගය, int අගය, size_t 바이트수);
#endif
