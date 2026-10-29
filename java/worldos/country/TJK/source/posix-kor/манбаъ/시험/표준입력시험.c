#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ворида_Рӯйхат) {
    (void)개수; (void)ворида_Рӯйхат;
    char иттилоот[6]; int дарозӣ_қимат = 0;
    puts("POSIX INPUT READY");
    while (дарозӣ_қимат < 6) {
        int 결과 = 파일자료읽기(0, иттилоот + дарозӣ_қимат, 6 - дарозӣ_қимат);
        if (결과 <= 0) return 1;
        дарозӣ_қимат += 결과;
    }
    if (memcmp(иттилоот, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
