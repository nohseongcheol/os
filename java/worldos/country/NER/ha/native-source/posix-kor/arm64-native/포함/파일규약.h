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
typedef int64_t Fayil_Sassautawa_rubuta;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fayil_Sassautawa_rubuta pk_lseek(int fd, Fayil_Sassautawa_rubuta offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fayil_Sassautawa_rubuta size);
int pk_fsync(int fd);
int pk_size(int fd);
int buɗe_Fayil(const char *Hanyar_shiga, int tsari_yanayin_aiki, ...);
입출력결과형 파일자료읽기(int Fayil, void *Tarin_bayani, size_t 개수);
입출력결과형 Rubuta_Fayil_Tarin_bayani(int Fayil, const void *Tarin_bayani, size_t 개수);
int Rufe_Fayil(int Fayil);
Fayil_Sassautawa_rubuta binciko_Fayil(int Fayil, Fayil_Sassautawa_rubuta 거리, int 기준);
int Cire_Fayil_Mashigar_bayanai_Suna(const char *Hanyar_shiga);
int zubi_Fayil_Tsawo(int Fayil, Fayil_Sassautawa_rubuta Girma);
int 파일저장확정(int Fayil);
int Fayil_girma(int Fayil);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define karanta_kawai_Daraja 0
#define 쓰기전용 1
#define Rubutuwa_karantuwa 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
