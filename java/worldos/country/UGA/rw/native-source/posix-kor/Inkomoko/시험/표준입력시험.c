#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **icyinjizwa_Urutonde) {
    (void)개수; (void)icyinjizwa_Urutonde;
    char amakurushingiro[6]; int uburebure_agaciro = 0;
    puts("POSIX INPUT READY");
    while (uburebure_agaciro < 6) {
        int 결과 = 파일자료읽기(0, amakurushingiro + uburebure_agaciro, 6 - uburebure_agaciro);
        if (결과 <= 0) return 1;
        uburebure_agaciro += 결과;
    }
    if (memcmp(amakurushingiro, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
