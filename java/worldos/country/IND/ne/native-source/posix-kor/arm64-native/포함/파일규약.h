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
typedef int64_t फाइल_अफसेट_प्रकार;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
फाइल_अफसेट_प्रकार pk_lseek(int fd, फाइल_अफसेट_प्रकार offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, फाइल_अफसेट_प्रकार size);
int pk_fsync(int fd);
int pk_size(int fd);
int सिर्जना_फाइल(const char *मार्ग, int तरिका_मोड, ...);
입출력결과형 파일자료읽기(int फाइल, void *लगत, size_t 개수);
입출력결과형 लेख्नुहोस्_फाइल_लगत(int फाइल, const void *लगत, size_t 개수);
int बन्द_गर्नुहोस्_फाइल(int फाइल);
फाइल_अफसेट_प्रकार खोज्नुहोस्_फाइल(int फाइल, फाइल_अफसेट_प्रकार 거리, int परियोजना_रूट);
int हटाउनुहोस्_फाइल_प्रविष्टि_नाम(const char *मार्ग);
int सेट_फाइल_लम्बाइ(int फाइल, फाइल_अफसेट_प्रकार आकार);
int 파일저장확정(int फाइल);
int फाइल_साइज(int फाइल);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define पढ्न_मात्र_मान 0
#define 쓰기전용 1
#define पढ्न_लेख्_न 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
