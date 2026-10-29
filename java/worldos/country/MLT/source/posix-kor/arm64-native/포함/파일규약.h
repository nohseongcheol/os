#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_COUNT_TYPE;
typedef int64_t fajl_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fajl_OFFSET_TYPE pk_lseek(int fd, fajl_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fajl_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int fetaħ_fajl(const char *mogħdija, int metodu_MODE, ...);
입출력결과형 파일자료읽기(int fajl, void *data, size_t element_COUNT);
입출력결과형 kiteb_fajl_data(int fajl, const void *data, size_t element_COUNT);
int agħlaq_fajl(int fajl);
fajl_OFFSET_TYPE fittex_fajl(int fajl, fajl_OFFSET_TYPE 거리, int pprojetta_għerq);
int neħħa_fajl_entrata_isem(const char *mogħdija);
int sett_fajl_tul(int fajl, fajl_OFFSET_TYPE daqqas);
int 파일저장확정(int fajl);
int fajl_daqqas(int fajl);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define qari_biss_VALUE 0
#define 쓰기전용 1
#define qari_kitba 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
