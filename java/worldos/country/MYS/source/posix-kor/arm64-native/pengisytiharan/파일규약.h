#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bait_COUNT_TYPE;
typedef int64_t fail_Ofset_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fail_Ofset_TYPE pk_lseek(int fd, fail_Ofset_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fail_Ofset_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int buka_fail(const char *LALUAN, int kaedah_mod, ...);
입출력결과형 파일자료읽기(int Fail, void *data, size_t item_COUNT);
입출력결과형 tulis_fail_data(int Fail, const void *data, size_t item_COUNT);
int Tutup_fail(int Fail);
fail_Ofset_TYPE cari_fail(int Fail, fail_Ofset_TYPE 거리, int projek_akar);
int alih_keluar_fail_pemasukan_nama(const char *LALUAN);
int set_fail_kepanjangan(int Fail, fail_Ofset_TYPE Saiz);
int lakukan_storan_fail(int Fail);
int saiz_fail(int Fail);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define baca_sahaja_VALUE 0
#define tulis_sahaja_VALUE 1
#define baca_tulis 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define potong_TOC 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
