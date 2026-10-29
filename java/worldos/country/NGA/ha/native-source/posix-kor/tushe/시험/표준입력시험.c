#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **Mashigar_bayanai_Jeri) {
    (void)개수; (void)Mashigar_bayanai_Jeri;
    char Tarin_bayani[6]; int Tsawo_Daraja = 0;
    puts("POSIX INPUT READY");
    while (Tsawo_Daraja < 6) {
        int 결과 = 파일자료읽기(0, Tarin_bayani + Tsawo_Daraja, 6 - Tsawo_Daraja);
        if (결과 <= 0) return 1;
        Tsawo_Daraja += 결과;
    }
    if (memcmp(Tarin_bayani, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
