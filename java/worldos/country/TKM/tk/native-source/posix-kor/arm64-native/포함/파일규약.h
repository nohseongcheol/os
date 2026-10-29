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
typedef int64_t faýl_Süýşüriş_ýaz;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
faýl_Süýşüriş_ýaz pk_lseek(int fd, faýl_Süýşüriş_ýaz offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, faýl_Süýşüriş_ýaz size);
int pk_fsync(int fd);
int pk_size(int fd);
int aç_faýl(const char *Ýol, int usul_reje, ...);
입출력결과형 파일자료읽기(int Faýl, void *maglumat, size_t 개수);
입출력결과형 ýaz_faýl_maglumat(int Faýl, const void *maglumat, size_t 개수);
int ýap_faýl(int Faýl);
faýl_Süýşüriş_ýaz gözle_faýl(int Faýl, faýl_Süýşüriş_ýaz 거리, int 기준);
int aýyr_faýl_girizmeklik_at(const char *Ýol);
int köplük_faýl_dowamlylyk(int Faýl, faýl_Süýşüriş_ýaz Ululyk);
int 파일저장확정(int Faýl);
int faýl_ölçegi_üýtget(int Faýl);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define diňe_okalýan_baha 0
#define 쓰기전용 1
#define okalýan_ýazylýan 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
