#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define បើក_ឯកសារ open
#define បង្កើត_ឯកសារ creat
#define 파일자료읽기 read
#define សរសេរ_ឯកសារ_ទិន្នន័យ write
#define បិទ_ឯកសារ close
#define ស្វែងរក_ឯកសារ lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define យកចេញ_ឯកសារ_ការបញ្ចូល_ឈ្មោះ unlink
#define កំណត់_ឯកសារ_ប្រវែង ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define ដែលបានត្រឹមតែអាន_តំលៃ O_RDONLY
#define 쓰기전용 O_WRONLY
#define អាន_សរសេរ O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define ឯកសារ_ភាព stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល;
#endif
