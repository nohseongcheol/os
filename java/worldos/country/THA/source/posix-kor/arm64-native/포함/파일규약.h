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
typedef int64_t แฟ้ม_ออฟเซต_ชนิด;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
แฟ้ม_ออฟเซต_ชนิด pk_lseek(int fd, แฟ้ม_ออฟเซต_ชนิด offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, แฟ้ม_ออฟเซต_ชนิด size);
int pk_fsync(int fd);
int pk_size(int fd);
int เปิด_แฟ้ม(const char *เส้นทาง, int เมธอด_โหมด, ...);
입출력결과형 파일자료읽기(int แฟ้ม, void *ข้อมูล, size_t 개수);
입출력결과형 파일자료쓰기(int แฟ้ม, const void *ข้อมูล, size_t 개수);
int ปิด_แฟ้ม(int แฟ้ม);
แฟ้ม_ออฟเซต_ชนิด กรอ_แฟ้ม(int แฟ้ม, แฟ้ม_ออฟเซต_ชนิด 거리, int แสดง_ราก);
int นําออก_แฟ้ม_รายการ_ชื่อ(const char *เส้นทาง);
int 파일길이정하기(int แฟ้ม, แฟ้ม_ออฟเซต_ชนิด ขนาด);
int 파일저장확정(int แฟ้ม);
int ขนาดแฟ้ม(int แฟ้ม);
#ifdef __cplusplus
}
#endif
#define หมายเลขข้อผิดพลาด (*pk_errno_location())
#define อ่านอย่างเดียว_ค่า 0
#define แบบเขียนอย่างเดียว_ค่า 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define ปัจจุบัน_ราก 1
#define 끝기준 2
#endif
