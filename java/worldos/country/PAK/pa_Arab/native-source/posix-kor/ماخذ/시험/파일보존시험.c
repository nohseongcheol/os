#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **داخلہ_فرست) {
    (void)개수; (void)داخلہ_فرست;
    int فائل = بنڑاؤ_فائل("stored.txt", پڑھو_لکھو | 없으면만들기 | 내용비우기, 0600);
    if (فائل < 0 || لکھو_فائل_کوائف(فائل, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(فائل) < 0) return 2;
    if (بند_کرو_فائل(فائل) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
