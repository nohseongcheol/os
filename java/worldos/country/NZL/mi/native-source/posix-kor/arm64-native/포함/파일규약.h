#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t paita_COUNT_TYPE;
typedef int64_t kōnae_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
kōnae_OFFSET_TYPE pk_lseek(int fd, kōnae_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, kōnae_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int tiwhikete_kōnae(const char *ara, int aratuka_MODE, ...);
입출력결과형 파일자료읽기(int Kōnae, void *raraunga, size_t tuemi_COUNT);
입출력결과형 tuhi_kōnae_raraunga(int Kōnae, const void *raraunga, size_t tuemi_COUNT);
int kati_kōnae(int Kōnae);
kōnae_OFFSET_TYPE kimi_kōnae(int Kōnae, kōnae_OFFSET_TYPE 거리, int whakaatu_pūtake);
int tango_kōnae_tāurunga_ingoa(const char *ara);
int huinga_kōnae_roa(int Kōnae, kōnae_OFFSET_TYPE rahi);
int 파일저장확정(int Kōnae);
int kōnae_rahi(int Kōnae);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define pānui_anake_uara 0
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
