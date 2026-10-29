#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define fosgail_faidhle open
#define Create_faidhle creat
#define 파일자료읽기 read
#define sgrìobh_faidhle_dàta write
#define dùin_faidhle close
#define sir_faidhle lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define thoir_air_falbh_faidhle_cur_a_steach_ainm unlink
#define seata_faidhle_faid ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define ri_leughadh_a_mhàin_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define so_leughte_so_sgrìobhte O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define faidhle_cor stat
typedef size_t baidht_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t faidhle_OFFSET_TYPE;
#endif
