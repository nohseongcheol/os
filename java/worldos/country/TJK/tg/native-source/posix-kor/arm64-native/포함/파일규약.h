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
typedef int64_t файл_Интиқолшавӣ_навъ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_Интиқолшавӣ_навъ pk_lseek(int fd, файл_Интиқолшавӣ_навъ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_Интиқолшавӣ_навъ size);
int pk_fsync(int fd);
int pk_size(int fd);
int кушодан_файл(const char *масир, int сабк_ҳолат, ...);
입출력결과형 파일자료읽기(int Файл, void *иттилоот, size_t 개수);
입출력결과형 навиштан_файл_иттилоот(int Файл, const void *иттилоот, size_t 개수);
int пӯшидан_файл(int Файл);
файл_Интиқолшавӣ_навъ ҷустан_файл(int Файл, файл_Интиқолшавӣ_навъ 거리, int 기준);
int тоза_кардан_файл_ворида_ном(const char *масир);
int маҷмуъ_файл_дарозӣ(int Файл, файл_Интиқолшавӣ_навъ андоза_кардан);
int 파일저장확정(int Файл);
int файл_андоза_кардан(int Файл);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define танҳо_барои_хондан_қимат 0
#define 쓰기전용 1
#define хондан_навиштан 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
