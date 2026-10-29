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
typedef int64_t ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល pk_lseek(int fd, ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល size);
int pk_fsync(int fd);
int pk_size(int fd);
int បើក_ឯកសារ(const char *ផ្លូវ, int វិធីសាស្រ្ត_ម៉ូដ, ...);
입출력결과형 파일자료읽기(int ឯកសារ, void *ទិន្នន័យ, size_t 개수);
입출력결과형 សរសេរ_ឯកសារ_ទិន្នន័យ(int ឯកសារ, const void *ទិន្នន័យ, size_t 개수);
int បិទ_ឯកសារ(int ឯកសារ);
ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល ស្វែងរក_ឯកសារ(int ឯកសារ, ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល 거리, int បញ្ចាំង_ឬស);
int យកចេញ_ឯកសារ_ការបញ្ចូល_ឈ្មោះ(const char *ផ្លូវ);
int កំណត់_ឯកសារ_ប្រវែង(int ឯកសារ, ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល ដាក់ទំហំ);
int 파일저장확정(int ឯកសារ);
int ឯកសារ_ដាក់ទំហំ(int ឯកសារ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ដែលបានត្រឹមតែអាន_តំលៃ 0
#define 쓰기전용 1
#define អាន_សរសេរ 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
