#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **okufakwayo_Uhlu) {
    (void)개수; (void)okufakwayo_Uhlu;
    char imininingwane[6]; int ubude_inani = 0;
    puts("POSIX INPUT READY");
    while (ubude_inani < 6) {
        int 결과 = 파일자료읽기(0, imininingwane + ubude_inani, 6 - ubude_inani);
        if (결과 <= 0) return 1;
        ubude_inani += 결과;
    }
    if (memcmp(imininingwane, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
