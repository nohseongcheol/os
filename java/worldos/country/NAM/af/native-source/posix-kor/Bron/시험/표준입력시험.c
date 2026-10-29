#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int item_COUNT, char **inskrywing_Lys) {
    (void)item_COUNT; (void)inskrywing_Lys;
    char data[6]; int lengte_VALUE = 0;
    puts("POSIX INPUT READY");
    while (lengte_VALUE < 6) {
        int maatreël = 파일자료읽기(0, data + lengte_VALUE, 6 - lengte_VALUE);
        if (maatreël <= 0) return 1;
        lengte_VALUE += maatreël;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
