#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define பயனர்_படம்_முடி 0x02c00000ul
#define பயனர்_குவியல்_முடி 0x02ed0000ul
#define பயனர்_அடுக்கு_முகவரி 0x02f00000ul
#define பயனர்_முடி 0x03000000ul
#define 사용자쪽수 ((பயனர்_முடி - 사용자바탕) / 4096ul)
#define பயனர்_செயல்படுத்தக்கூடிய_கோப்பு_பிழை (-8)
#define பயனர்_தரவு_பிழை (-1001)
#define 사용자실행오류 (-1002)
#define பயனர்_செல்லுபடியாகாத_ஆணை (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t பதிவு_செய்_தரவு[31], கட்டளை_நிலை, நிலை_குறியீடு, அடுக்கு_முகவரி; } பயனர்_ஃபிரேம்;
void 사용자체계준비(void);
int பயனர்_விதிவிலக்கு(பயனர்_ஃபிரேம் *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t போர்டு_பயனர்_இயக்கு(uintptr_t);
uintptr_t போர்டு_பயனர்_சரிபார்(void);
uintptr_t போர்டு_பயனர்_கட்டுப்பாடு(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
