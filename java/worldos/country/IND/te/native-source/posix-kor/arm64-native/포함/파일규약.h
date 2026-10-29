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
typedef int64_t ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి pk_lseek(int fd, ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి size);
int pk_fsync(int fd);
int pk_size(int fd);
int తెరువు_ఫైలు(const char *పాత్, int విధానం_మోడ్_3f5e5497, ...);
입출력결과형 파일자료읽기(int దస్త్రం, void *డేటా, size_t 개수);
입출력결과형 వ్రాయి_ఫైలు_డేటా(int దస్త్రం, const void *డేటా, size_t 개수);
int మూసివేయి_ఫైలు(int దస్త్రం);
ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి శోధించు_ఫైలు(int దస్త్రం, ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి 거리, int ప్రొజెక్ట్_మూలం);
int తీసివెయ్యి_ఫైలు_ప్రవేశం_పేరు(const char *పాత్);
int సెట్_ఫైలు_పొడవు(int దస్త్రం, ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి పరిమాణం);
int 파일저장확정(int దస్త్రం);
int ఫైలు_పరిమాణం_మార్చు(int దస్త్రం);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define చదవడానికి_మాత్రమే_మూల్యం 0
#define 쓰기전용 1
#define పఠన_లేఖన 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
