#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t Byte_COUNT_TYPE;
typedef int64_t Fichier_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fichier_OFFSET_TYPE pk_lseek(int fd, Fichier_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fichier_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int ariichten_Fichier(const char *Wee, int Method_MODE, ...);
입출력결과형 파일자료읽기(int Fichier, void *Daten, size_t Element_COUNT);
입출력결과형 schreiwen_Fichier_Daten(int Fichier, const void *Daten, size_t Element_COUNT);
int Clôture_Fichier(int Fichier);
Fichier_OFFSET_TYPE sichen_Fichier(int Fichier, Fichier_OFFSET_TYPE 거리, int projezéieren_Racinn);
int ewechhuelen_Fichier_Agab_Numm(const char *Wee);
int Saz_Fichier_Längt(int Fichier, Fichier_OFFSET_TYPE d_Gréisst_veränneren);
int 파일저장확정(int Fichier);
int Fichier_d_Gréisst_veränneren(int Fichier);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define schreifgeschützt_VALUE 0
#define 쓰기전용 1
#define lies_schreiffäeg 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
