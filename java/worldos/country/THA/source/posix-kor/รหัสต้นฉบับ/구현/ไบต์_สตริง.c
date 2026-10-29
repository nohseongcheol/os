#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *สตริง_ค่า) { size_t 길이 = 0; while (สตริง_ค่า[길이]) 길이++; return 길이; }
int strcmp(const char *กล้องหน้า_ค่า, const char *ย้อนกลับ_ค่า) {
    while (*กล้องหน้า_ค่า && *กล้องหน้า_ค่า == *ย้อนกลับ_ค่า) { กล้องหน้า_ค่า++; ย้อนกลับ_ค่า++; }
    return (unsigned char)*กล้องหน้า_ค่า - (unsigned char)*ย้อนกลับ_ค่า;
}
int memcmp(const void *กล้องหน้า_ค่า, const void *ย้อนกลับ_ค่า, size_t 바이트수) {
    const unsigned char *가 = กล้องหน้า_ค่า, *나 = ย้อนกลับ_ค่า;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *ปลายทาง_ค่า_a0fbc067, const void *원본, size_t 바이트수) {
    unsigned char *가 = ปลายทาง_ค่า_a0fbc067; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return ปลายทาง_ค่า_a0fbc067;
}
void *memset(void *ปลายทาง_ค่า_a0fbc067, int ค่า, size_t 바이트수) {
    unsigned char *ข้อมูล = ปลายทาง_ค่า_a0fbc067;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) ข้อมูล[칸] = ค่า;
    return ปลายทาง_ค่า_a0fbc067;
}
int putchar(int 문자) { unsigned char ค่า = 문자; return write(1, &ค่า, 1) == 1 ? ค่า : EOF; }
int puts(const char *สตริง_ค่า) {
    size_t 길이 = strlen(สตริง_ค่า), ตําแหน่ง = 0;
    while (ตําแหน่ง < 길이) { ssize_t ผลลัพธ์ = write(1, สตริง_ค่า + ตําแหน่ง, 길이 - ตําแหน่ง); if (ผลลัพธ์ <= 0) return EOF; ตําแหน่ง += ผลลัพธ์; }
    return putchar('\n') == EOF ? EOF : 0;
}
