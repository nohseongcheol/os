#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define buat_file open
#define Buat_file creat
#define 파일자료읽기 read
#define tulis_file_data write
#define Tutup_file close
#define cari_file lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define hapus_file_entri_nama unlink
#define set_file_panjang ftruncate
#define penerapan_Files fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define baca_saja_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define baca_tulis O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define saat_ini_akar SEEK_CUR
#define 끝기준 SEEK_END
#define status_berkas stat
typedef size_t byte_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t file_OFFSET_TYPE;
#endif
