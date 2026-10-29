#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t 바이트수형;
typedef int64_t फ़ाइल_ऑफ़सेट_लिखें;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
फ़ाइल_ऑफ़सेट_लिखें pk_lseek(int fd, फ़ाइल_ऑफ़सेट_लिखें offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, फ़ाइल_ऑफ़सेट_लिखें size);
int pk_fsync(int fd);
int pk_size(int fd);
int जारी_फ़ाइल(const char *पथ, int विधि_मोड, ...);
입출력결과형 पढें_फ़ाइल_डेटा(int संचिका, void *आँकड़े, size_t 개수);
입출력결과형 लिखना_फ़ाइल_डेटा(int संचिका, const void *आँकड़े, size_t 개수);
int बंद_फ़ाइल(int संचिका);
फ़ाइल_ऑफ़सेट_लिखें खोजें_फ़ाइल(int संचिका, फ़ाइल_ऑफ़सेट_लिखें 거리, int प्रोजेक्ट_करें_मूल);
int निकालें_फ़ाइल_एन्ट्री_नाम(const char *पथ);
int 파일길이정하기(int संचिका, फ़ाइल_ऑफ़सेट_लिखें आकार);
int कमिट_फ़ाइल_संग्रहण(int संचिका);
int फ़ाइल_आकार(int संचिका);
#ifdef __cplusplus
}
#endif
#define त्रुटि_संख्या (*pk_errno_location())
#define केवल_पढ़ने_के_लिए_मान 0
#define सिर्फ_लिखे_मान 1
#define पठन_लेखन 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define कम_करें_सामग्री 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define अद्यतित_मूल 1
#define 끝기준 2
#endif
