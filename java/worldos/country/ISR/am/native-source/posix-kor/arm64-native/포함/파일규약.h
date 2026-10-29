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
typedef int64_t ፋይል_ዝንፍ_ተይብ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ፋይል_ዝንፍ_ተይብ pk_lseek(int fd, ፋይል_ዝንፍ_ተይብ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ፋይል_ዝንፍ_ተይብ size);
int pk_fsync(int fd);
int pk_size(int fd);
int ክፈት_ፋይል(const char *መተላለፊያ, int ስልት_ሁነታ, ...);
입출력결과형 파일자료읽기(int ፋይል, void *ውሂብ, size_t 개수);
입출력결과형 ጻፍ_ፋይል_ውሂብ(int ፋይል, const void *ውሂብ, size_t 개수);
int ዝጋ_ፋይል(int ፋይል);
ፋይል_ዝንፍ_ተይብ ፈልግ_ፋይል(int ፋይል, ፋይል_ዝንፍ_ተይብ 거리, int አሳይ_ስር);
int አስወግድ_ፋይል_ምዝግብ_ስም(const char *መተላለፊያ);
int ስብስብ_ፋይል_ርዝመት(int ፋይል, ፋይል_ዝንፍ_ተይብ መጠን);
int 파일저장확정(int ፋይል);
int ፋይል_መጠን_ቀይር(int ፋይል);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ተነባቢ_ብቻ_እሴት 0
#define 쓰기전용 1
#define ተነባቢ_የሚጻፍበት 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
