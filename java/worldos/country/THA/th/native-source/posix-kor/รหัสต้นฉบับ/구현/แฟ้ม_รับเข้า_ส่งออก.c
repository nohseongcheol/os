#include <파일규약.h>
#include "호출경계.h"

int หมายเลขข้อผิดพลาด;
int 호출결과(int ผลลัพธ์) {
    if (ผลลัพธ์ < 0) { หมายเลขข้อผิดพลาด = -ผลลัพธ์; return -1; }
    return ผลลัพธ์;
}
int open(const char *แฟ้ม_รายการ_ชื่อ, int เปิด_การตั้งค่า, ...) {
    mode_t 허가 = 0;
    if (เปิด_การตั้งค่า & O_CREAT) {
        __builtin_va_list อาร์กิวเมนต์;
        __builtin_va_start(อาร์กิวเมนต์, เปิด_การตั้งค่า);
        허가 = __builtin_va_arg(อาร์กิวเมนต์, mode_t);
        __builtin_va_end(อาร์กิวเมนต์);
    }
    return 호출결과(jkoros_syscall(30, (int)แฟ้ม_รายการ_ชื่อ, เปิด_การตั้งค่า, 허가, 0, 0));
}
int creat(const char *แฟ้ม_รายการ_ชื่อ, mode_t 허가) { return open(แฟ้ม_รายการ_ชื่อ, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ข้อมูล, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ข้อมูล, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ข้อมูล, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ข้อมูล, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ออฟเซต_ค่า, int แสดง_ราก) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ออฟเซต_ค่า, แสดง_ราก, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *สถานะ_ค่า) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)สถานะ_ค่า, 0, 0, 0)); }
int unlink(const char *แฟ้ม_รายการ_ชื่อ) { return 호출결과(jkoros_syscall(38, (int)แฟ้ม_รายการ_ชื่อ, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int คําสั่ง, ...) {
    int ค่า = 0;
    if (คําสั่ง == F_DUPFD || คําสั่ง == F_DUPFD_CLOEXEC || คําสั่ง == F_SETFD || คําสั่ง == F_SETFL) {
        __builtin_va_list อาร์กิวเมนต์;
        __builtin_va_start(อาร์กิวเมนต์, คําสั่ง); ค่า = __builtin_va_arg(อาร์กิวเมนต์, int); __builtin_va_end(อาร์กิวเมนต์);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, คําสั่ง, ค่า, 0, 0));
}
