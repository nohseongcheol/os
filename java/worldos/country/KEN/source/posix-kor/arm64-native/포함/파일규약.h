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
typedef int64_t faili_Chipua_aina;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
faili_Chipua_aina pk_lseek(int fd, faili_Chipua_aina offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, faili_Chipua_aina size);
int pk_fsync(int fd);
int pk_size(int fd);
int unda_faili(const char *njia, int mbinu_hali_tumizi, ...);
입출력결과형 파일자료읽기(int faili, void *data, size_t 개수);
입출력결과형 andika_faili_data(int faili, const void *data, size_t 개수);
int funga_faili(int faili);
faili_Chipua_aina tafuta_faili(int faili, faili_Chipua_aina 거리, int 기준);
int ondoa_faili_ingizo_jina(const char *njia);
int seti_faili_urefu(int faili, faili_Chipua_aina panga_ukubwa);
int 파일저장확정(int faili);
int faili_panga_ukubwa(int faili);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define soma_tu_thamani 0
#define 쓰기전용 1
#define soma_andika 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
