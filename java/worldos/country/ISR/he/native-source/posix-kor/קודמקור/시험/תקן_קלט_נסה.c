#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ערך_רשימה) {
    (void)개수; (void)ערך_רשימה;
    char נתונים[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int תוצאה = 파일자료읽기(0, נתונים + 길이, 6 - 길이);
        if (תוצאה <= 0) return 1;
        길이 += תוצאה;
    }
    if (memcmp(נתונים, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
