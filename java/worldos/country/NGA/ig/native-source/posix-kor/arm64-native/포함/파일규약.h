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
typedef int64_t ọbọakwụkwọ_Nnokwata_pinye;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ọbọakwụkwọ_Nnokwata_pinye pk_lseek(int fd, ọbọakwụkwọ_Nnokwata_pinye offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ọbọakwụkwọ_Nnokwata_pinye size);
int pk_fsync(int fd);
int pk_size(int fd);
int mepee_ọbọakwụkwọ(const char *ụzọ_ozi, int usoro_moòdù, ...);
입출력결과형 파일자료읽기(int Faịlụ, void *datà, size_t 개수);
입출력결과형 dee_ọbọakwụkwọ_datà(int Faịlụ, const void *datà, size_t 개수);
int mmechi_ọbọakwụkwọ(int Faịlụ);
ọbọakwụkwọ_Nnokwata_pinye ọchịchọ_ọbọakwụkwọ(int Faịlụ, ọbọakwụkwọ_Nnokwata_pinye 거리, int 기준);
int wepụ_ọbọakwụkwọ_ndebà_akara_ahà(const char *ụzọ_ozi);
int Seti_ọbọakwụkwọ_ogologo(int Faịlụ, ọbọakwụkwọ_Nnokwata_pinye Ụhara);
int 파일저장확정(int Faịlụ);
int ọbọakwụkwọ_ụha(int Faịlụ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ọgụgụ_naanị_valuu 0
#define 쓰기전용 1
#define gụọ_dèe 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
