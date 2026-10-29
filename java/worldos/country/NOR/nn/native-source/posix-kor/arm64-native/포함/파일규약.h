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
typedef int64_t fil_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fil_OFFSET_TYPE pk_lseek(int fd, fil_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fil_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int opne_fil(const char *STIGE, int metode_MODE, ...);
입출력결과형 파일자료읽기(int Fil, void *data, size_t vare_COUNT);
입출력결과형 skrive_fil_data(int Fil, const void *data, size_t vare_COUNT);
int Lukk_fil(int Fil);
fil_OFFSET_TYPE søk_fil(int Fil, fil_OFFSET_TYPE 거리, int spegle_rot);
int fjerne_fil_oppføring_namn(const char *STIGE);
int sett_fil_lengd(int Fil, fil_OFFSET_TYPE Storleik);
int 파일저장확정(int Fil);
int fil_endre_storleik(int Fil);
#ifdef __cplusplus
}
#endif
#define feilnummer (*pk_errno_location())
#define skriveverna_VALUE 0
#define 쓰기전용 1
#define lese_og_skrivetilgang 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define betalt_rot 1
#define avslutte_nullpunkt 2
#endif
