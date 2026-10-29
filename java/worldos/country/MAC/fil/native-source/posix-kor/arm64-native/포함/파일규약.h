#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_COUNT_TYPE;
typedef int64_t file_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
file_OFFSET_TYPE pk_lseek(int fd, file_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, file_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int buksan_file(const char *path, int pamamaraan_MODE, ...);
입출력결과형 파일자료읽기(int file, void *data, size_t item_COUNT);
입출력결과형 sumulat_file_data(int file, const void *data, size_t item_COUNT);
int isara_file(int file);
file_OFFSET_TYPE i_seek_file(int file, file_OFFSET_TYPE 거리, int Project_root);
int tanggalin_file_pagpasok_pangalan(const char *path);
int set_file_haba(int file, file_OFFSET_TYPE sukat_82232621);
int 파일저장확정(int file);
int file_sukat(int file);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define mababasa_lamang_VALUE 0
#define 쓰기전용 1
#define nababasa_nasusulatan 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
