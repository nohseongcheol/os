#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **go_tsenya_tshedimošo_Lenaneo) {
    (void)개수; (void)go_tsenya_tshedimošo_Lenaneo;
    char data[6]; int botelele_boleng = 0;
    puts("POSIX INPUT READY");
    while (botelele_boleng < 6) {
        int 결과 = 파일자료읽기(0, data + botelele_boleng, 6 - botelele_boleng);
        if (결과 <= 0) return 1;
        botelele_boleng += 결과;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
