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
typedef int64_t faele_E_Šetšego_thaepa;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
faele_E_Šetšego_thaepa pk_lseek(int fd, faele_E_Šetšego_thaepa offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, faele_E_Šetšego_thaepa size);
int pk_fsync(int fd);
int pk_size(int fd);
int bula_faele(const char *Tsejana, int mokgwa_mokgwa, ...);
입출력결과형 파일자료읽기(int Faele, void *data, size_t 개수);
입출력결과형 ngwala_faele_data(int Faele, const void *data, size_t 개수);
int tswalela_faele(int Faele);
faele_E_Šetšego_thaepa nyaka_faele(int Faele, faele_E_Šetšego_thaepa 거리, int 기준);
int tloša_faele_go_tsenya_tshedimošo_leina(const char *Tsejana);
int sehlopha_faele_botelele(int Faele, faele_E_Šetšego_thaepa Bogolo);
int 파일저장확정(int Faele);
int faele_bogolo(int Faele);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define balwago_fela_boleng 0
#define 쓰기전용 1
#define bala_ngwala 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
