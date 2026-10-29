#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **รายการ_รายการ) {
    (void)개수; (void)รายการ_รายการ;
    char ข้อมูล[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int ผลลัพธ์ = 파일자료읽기(0, ข้อมูล + 길이, 6 - 길이);
        if (ผลลัพธ์ <= 0) return 1;
        길이 += ผลลัพธ์;
    }
    if (memcmp(ข้อมูล, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
