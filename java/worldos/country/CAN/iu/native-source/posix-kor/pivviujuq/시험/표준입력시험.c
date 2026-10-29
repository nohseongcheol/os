#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **Iliniku_Titiqpalliagaq) {
    (void)개수; (void)Iliniku_Titiqpalliagaq;
    char titiqqat[6]; int takininga_atuutilik = 0;
    puts("POSIX INPUT READY");
    while (takininga_atuutilik < 6) {
        int 결과 = 파일자료읽기(0, titiqqat + takininga_atuutilik, 6 - takininga_atuutilik);
        if (결과 <= 0) return 1;
        takininga_atuutilik += 결과;
    }
    if (memcmp(titiqqat, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
