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
typedef int64_t 파일위치형;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
파일위치형 pk_lseek(int fd, 파일위치형 offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, 파일위치형 size);
int pk_fsync(int fd);
int pk_size(int fd);
int 파일열기(const char *경로, int 방식, ...);
입출력결과형 파일자료읽기(int COADAN, void *자료, size_t 개수);
입출력결과형 파일자료쓰기(int COADAN, const void *자료, size_t 개수);
int 파일닫기(int COADAN);
파일위치형 파일위치옮기기(int COADAN, 파일위치형 거리, int 기준);
int 파일이름지우기(const char *경로);
int 파일길이정하기(int COADAN, 파일위치형 크기);
int 파일저장확정(int COADAN);
int 파일크기(int COADAN);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define 읽기전용 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
