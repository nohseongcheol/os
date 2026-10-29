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
typedef int64_t ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ pk_lseek(int fd, ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ size);
int pk_fsync(int fd);
int pk_size(int fd);
int ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ(const char *ਮਾਰਗ, int ਮੈਥਡ_ਮੋਡ, ...);
입출력결과형 파일자료읽기(int ਫਾਇਲ, void *ਸਮੱਗਰੀ, size_t 개수);
입출력결과형 ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(int ਫਾਇਲ, const void *ਸਮੱਗਰੀ, size_t 개수);
int ਬੰਦ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ(int ਫਾਇਲ);
ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ ਸੀਕ_ਲਿਖਤ_ਪੱਤਰ(int ਫਾਇਲ, ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ 거리, int ਪ੍ਰੋਜੈਕਟ_ਰੂਟ);
int ਹਟਾਉਣਾ_ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ(const char *ਮਾਰਗ);
int ਸੈਟ_ਲਿਖਤ_ਪੱਤਰ_ਲੰਬਾਈ(int ਫਾਇਲ, ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ ਆਕਾਰ);
int 파일저장확정(int ਫਾਇਲ);
int ਲਿਖਤ_ਪੱਤਰ_ਆਕਾਰ(int ਫਾਇਲ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ 0
#define 쓰기전용 1
#define ਪੜ੍ਹਨ_ਲਿਖਣ 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
