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
typedef int64_t ھۆججەت_ئاغما_تىپ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ھۆججەت_ئاغما_تىپ pk_lseek(int fd, ھۆججەت_ئاغما_تىپ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ھۆججەت_ئاغما_تىپ size);
int pk_fsync(int fd);
int pk_size(int fd);
int قۇرۇش_ھۆججەت(const char *يول, int ئۇسۇل_ھالەت, ...);
입출력결과형 파일자료읽기(int ھۆججەت, void *مەلۇمات, size_t 개수);
입출력결과형 يازماق_ھۆججەت_مەلۇمات(int ھۆججەت, const void *مەلۇمات, size_t 개수);
int ئاياغ_ھۆججەت(int ھۆججەت);
ھۆججەت_ئاغما_تىپ ئىزدەش_ھۆججەت(int ھۆججەت, ھۆججەت_ئاغما_تىپ 거리, int كۆرسىتىش_يىلتىز);
int چىقىرىۋەتمەك_ھۆججەت_كىرگۈزۈش_نامى(const char *يول);
int توپ_ھۆججەت_ئۇزۇنلۇق(int ھۆججەت, ھۆججەت_ئاغما_تىپ چوڭلۇقى);
int 파일저장확정(int ھۆججەت);
int ھۆججەت_ئۆزگەرتمەك(int ھۆججەت);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ئوقۇشقىلا_بولىدىغان_قىممىتى 0
#define 쓰기전용 1
#define ئوقۇش_يېزىش 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
