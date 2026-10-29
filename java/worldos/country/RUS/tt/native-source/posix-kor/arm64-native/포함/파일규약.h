#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t байт_COUNT_TYPE;
typedef int64_t файл_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_OFFSET_TYPE pk_lseek(int fd, файл_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int ачу_файл(const char *Yul, int ысул_MODE, ...);
입출력결과형 파일자료읽기(int Birem, void *мәгълүмат, size_t элемент_COUNT);
입출력결과형 язу_файл_мәгълүмат(int Birem, const void *мәгълүмат, size_t элемент_COUNT);
int чик_файл(int Birem);
файл_OFFSET_TYPE эзләү_файл(int Birem, файл_OFFSET_TYPE 거리, int экранга_җибәрү_тамыр);
int бетерү_файл_кертү_исем(const char *Yul);
int җыелма_файл_озынлык(int Birem, файл_OFFSET_TYPE үлчәмен_үзгәртү);
int 파일저장확정(int Birem);
int файл_үлчәмен_үзгәртү(int Birem);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define укымалы_гына_VALUE 0
#define 쓰기전용 1
#define укымалы_язмалы 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
