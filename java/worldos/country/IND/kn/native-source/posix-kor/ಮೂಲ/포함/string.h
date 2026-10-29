#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ);
int strcmp(const char *ಮುಂದೆ_ಮೌಲ್ಯ, const char *ಹಿಂದೆ_ಮೌಲ್ಯ);
int memcmp(const void *ಮುಂದೆ_ಮೌಲ್ಯ, const void *ಹಿಂದೆ_ಮೌಲ್ಯ, size_t 바이트수);
void *memcpy(void *ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ, const void *원본, size_t 바이트수);
void *memset(void *ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ, int ಮೌಲ್ಯ, size_t 바이트수);
#endif
