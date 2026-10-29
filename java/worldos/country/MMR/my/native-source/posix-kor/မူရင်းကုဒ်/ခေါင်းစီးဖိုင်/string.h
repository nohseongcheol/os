#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *အက္ခရာစဉ်);
int strcmp(const char *ရှေ့တန်ဖိုး, const char *နောက်တန်ဖိုး);
int memcmp(const void *ရှေ့တန်ဖိုး, const void *နောက်တန်ဖိုး, size_t ဘိုက်အရေအတွက်);
void *memcpy(void *ဦးတည်ရာတန်ဖိုး, const void *မူရင်း, size_t ဘိုက်အရေအတွက်);
void *memset(void *ဦးတည်ရာတန်ဖိုး, int တန်ဖိုး, size_t ဘိုက်အရေအတွက်);
#endif
