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
typedef int64_t ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା pk_lseek(int fd, ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା size);
int pk_fsync(int fd);
int pk_size(int fd);
int ଖୋଲିବା_ଫାଇଲ୍(const char *ପଥ, int ପଦ୍ଧତି_ମୋଡ୍, ...);
입출력결과형 파일자료읽기(int ଫାଇଲ, void *ଡାଟା, size_t 개수);
입출력결과형 ଲିଖନ_ଫାଇଲ୍_ଡାଟା(int ଫାଇଲ, const void *ଡାଟା, size_t 개수);
int ବନ୍ଦ_ଫାଇଲ୍(int ଫାଇଲ);
ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା ସୀକ୍_ଫାଇଲ୍(int ଫାଇଲ, ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା 거리, int ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍);
int ଅପସାରଣ_କରିବା_ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ(const char *ପଥ);
int ସେଟ୍_ଫାଇଲ୍_ଦୈର୍ଘ୍ୟ(int ଫାଇଲ, ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା ଆକାର);
int 파일저장확정(int ଫାଇଲ);
int ଫାଇଲ୍_ଅକାର(int ଫାଇଲ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ 0
#define 쓰기전용 1
#define ପଢିବା_ଲେଖିବା 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
