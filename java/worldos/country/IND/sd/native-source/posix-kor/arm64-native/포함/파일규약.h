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
typedef int64_t فائل_آف_سيٽ_قسم;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
فائل_آف_سيٽ_قسم pk_lseek(int fd, فائل_آف_سيٽ_قسم offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, فائل_آف_سيٽ_قسم size);
int pk_fsync(int fd);
int pk_size(int fd);
int ٺاھيو_فائل(const char *راههه, int طريقو_موڊ, ...);
입출력결과형 파일자료읽기(int فائل, void *ڪوائف, size_t 개수);
입출력결과형 لکو_فائل_ڪوائف(int فائل, const void *ڪوائف, size_t 개수);
int بند_ڪرڻ_فائل(int فائل);
فائل_آف_سيٽ_قسم ڳولا_فائل(int فائل, فائل_آف_سيٽ_قسم 거리, int 기준);
int هٽايو_فائل_داخلا_نالو(const char *راههه);
int سيٽ_فائل_لمبائي(int فائل, فائل_آف_سيٽ_قسم سائيز);
int 파일저장확정(int فائل);
int فائل_سائيز(int فائل);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define صرف_مطالعو_قدر 0
#define 쓰기전용 1
#define پڙهڻ_لکڻ 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
