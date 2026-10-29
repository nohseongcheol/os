#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *स्ट्रींग_मूल्य);
int strcmp(const char *पुढील_मूल्य, const char *मागे_मूल्य);
int memcmp(const void *पुढील_मूल्य, const void *मागे_मूल्य, size_t बाइट_संख्या);
void *memcpy(void *गंतव्यस्थान_मूल्य, const void *मूळ, size_t बाइट_संख्या);
void *memset(void *गंतव्यस्थान_मूल्य, int मूल्य, size_t बाइट_संख्या);
#endif
