#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int элемент_COUNT, char **кертү_Исемлек) {
    (void)элемент_COUNT; (void)кертү_Исемлек;
    char мәгълүмат[6]; int озынлык_VALUE = 0;
    puts("POSIX INPUT READY");
    while (озынлык_VALUE < 6) {
        int үлчәм = 파일자료읽기(0, мәгълүмат + озынлык_VALUE, 6 - озынлык_VALUE);
        if (үлчәм <= 0) return 1;
        озынлык_VALUE += үлчәм;
    }
    if (memcmp(мәгълүмат, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
