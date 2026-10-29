#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **naatnugol_Doggol) {
    (void)개수; (void)naatnugol_Doggol;
    char keɓe[6]; int njuuteendi_njaru = 0;
    puts("POSIX INPUT READY");
    while (njuuteendi_njaru < 6) {
        int 결과 = 파일자료읽기(0, keɓe + njuuteendi_njaru, 6 - njuuteendi_njaru);
        if (결과 <= 0) return 1;
        njuuteendi_njaru += 결과;
    }
    if (memcmp(keɓe, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
