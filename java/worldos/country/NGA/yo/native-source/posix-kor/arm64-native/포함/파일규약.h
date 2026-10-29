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
typedef int64_t fáìlì_Ìtayọ_irú;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fáìlì_Ìtayọ_irú pk_lseek(int fd, fáìlì_Ìtayọ_irú offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fáìlì_Ìtayọ_irú size);
int pk_fsync(int fd);
int pk_size(int fd);
int ṣí_fáìlì(const char *ọ̀nà, int ìlànà_móòdù, ...);
입출력결과형 파일자료읽기(int Fáìlì, void *détà, size_t 개수);
입출력결과형 kọ_fáìlì_détà(int Fáìlì, const void *détà, size_t 개수);
int pa_dé_fáìlì(int Fáìlì);
fáìlì_Ìtayọ_irú ṣàwárí_fáìlì(int Fáìlì, fáìlì_Ìtayọ_irú 거리, int 기준);
int ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ(const char *ọ̀nà);
int ọ̀wọ̀_fáìlì_gígùn(int Fáìlì, fáìlì_Ìtayọ_irú Ìwọ̀n);
int 파일저장확정(int Fáìlì);
int fáìlì_ìwọn(int Fáìlì);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define kàn_kàá_iye 0
#define 쓰기전용 1
#define tí_a_lè_kà_tí_a_lè_kọ 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
