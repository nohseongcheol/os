#include "string.h"
size_t strlen(const char *สตริง_ข้อมูล) { const char *ข้อมูล_ตําแหน่ง = สตริง_ข้อมูล; while (*ข้อมูล_ตําแหน่ง) ข้อมูล_ตําแหน่ง++; return ข้อมูล_ตําแหน่ง - สตริง_ข้อมูล; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *พิกัดแกน_x = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*พิกัดแกน_x != *세로좌표) return (int)*พิกัดแกน_x - *세로좌표; พิกัดแกน_x++; 세로좌표++; } return 0; }
void *memmove(void *ปลายทาง_ข้อมูล, const void *สตริง_ข้อมูล, size_t 개수) { unsigned char *พิกัดแกน_x = ปลายทาง_ข้อมูล; const unsigned char *세로좌표 = สตริง_ข้อมูล; if (พิกัดแกน_x < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) พิกัดแกน_x[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; พิกัดแกน_x[개수] = 세로좌표[개수]; } } return ปลายทาง_ข้อมูล; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char พิกัดแกน_x = *첫째값++, 세로좌표 = *둘째값++; if (พิกัดแกน_x != 세로좌표) return (int)พิกัดแกน_x-세로좌표; if (!พิกัดแกน_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *สตริง_ข้อมูล, char **สิ้นสุดการโทร_ออฟเซต, int พื้นหลัง_ค่า) {
    const char *เริ่ม_ออฟเซต = สตริง_ข้อมูล; unsigned long ค่า = 0; int การเข้ารหัส_ค่า = 1, 하나라도 = 0;
    while (*สตริง_ข้อมูล == ' ' || (*สตริง_ข้อมูล >= 9 && *สตริง_ข้อมูล <= 13)) สตริง_ข้อมูล++;
    if (*สตริง_ข้อมูล == '-' || *สตริง_ข้อมูล == '+') { if (*สตริง_ข้อมูล == '-') การเข้ารหัส_ค่า = -1; สตริง_ข้อมูล++; }
    if (พื้นหลัง_ค่า == 0) พื้นหลัง_ค่า = 10;
    while (*สตริง_ข้อมูล >= '0' && *สตริง_ข้อมูล <= '9' && *สตริง_ข้อมูล - '0' < พื้นหลัง_ค่า) {
        unsigned ตัวเลข_ค่า = *สตริง_ข้อมูล++ - '0'; 하나라도 = 1;
        if (ค่า > (0x7ffffffffffffffful - ตัวเลข_ค่า) / (unsigned)พื้นหลัง_ค่า) ค่า = 0x7ffffffffffffffful;
        else ค่า = ค่า * พื้นหลัง_ค่า + ตัวเลข_ค่า;
    }
    if (สิ้นสุดการโทร_ออฟเซต) *สิ้นสุดการโทร_ออฟเซต = (char *)(하나라도 ? สตริง_ข้อมูล : เริ่ม_ออฟเซต); return การเข้ารหัส_ค่า > 0 ? (long)ค่า : -(long)ค่า;
}
int atoi(const char *สตริง_ข้อมูล) { return (int)strtol(สตริง_ข้อมูล, 0, 10); }
