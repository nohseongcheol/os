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
typedef int64_t bara_denc_Randal_xeet;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
bara_denc_Randal_xeet pk_lseek(int fd, bara_denc_Randal_xeet offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, bara_denc_Randal_xeet size);
int pk_fsync(int fd);
int pk_size(int fd);
int sos_bara_denc(const char *Yoonu_jëmale, int doxalin_anam, ...);
입출력결과형 파일자료읽기(int bara_denc, void *mbir, size_t 개수);
입출력결과형 biir_bara_denc_mbir(int bara_denc, const void *mbir, size_t 개수);
int Tej_bara_denc(int bara_denc);
bara_denc_Randal_xeet seet_bara_denc(int bara_denc, bara_denc_Randal_xeet 거리, int 기준);
int dandal_bara_denc_dugal_xabaar_tur(const char *Yoonu_jëmale);
int Boole_gi_bara_denc_diir(int bara_denc, bara_denc_Randal_xeet tolluwaay);
int 파일저장확정(int bara_denc);
int bara_denc_tolluwaay(int bara_denc);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ngir_jaŋarek_la_xëyma 0
#define 쓰기전용 1
#define jàng_bind 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
