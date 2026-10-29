#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **รายการ_รายการ) {
    (void)개수; (void)รายการ_รายการ;
    int แฟ้ม = เปิด_แฟ้ม("stored.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (แฟ้ม < 0 || 파일자료쓰기(แฟ้ม, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(แฟ้ม) < 0) return 2;
    if (ปิด_แฟ้ม(แฟ้ม) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
