#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define buka_fail open
#define cipta_fail creat
#define 파일자료읽기 read
#define tulis_fail_data write
#define Tutup_fail close
#define cari_fail lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define alih_keluar_fail_pemasukan_nama unlink
#define set_fail_kepanjangan ftruncate
#define lakukan_storan_fail fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define baca_sahaja_VALUE O_RDONLY
#define tulis_sahaja_VALUE O_WRONLY
#define baca_tulis O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define potong_TOC O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define status_fail stat
typedef size_t bait_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t fail_Ofset_TYPE;
#endif
