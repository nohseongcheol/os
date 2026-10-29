#include "Ara_sınır.h"
extern int main(int 인수개수, char **bağımsız_değişken_Liste);
static char bağımsız_değişken_Bellek[2048];
static char *bağımsız_değişken_Liste[18];
int jkoros_main(void) {
    int öğe_BAĞ_DEĞ_SAY = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (öğe_BAĞ_DEĞ_SAY < 0 || öğe_BAĞ_DEĞ_SAY > 16) return 126;
    /* geçerli_öğe 커널의 argv는 yürütmek_komut 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    bağımsız_değişken_Liste[0] = "jkoros-app";
    int konum = 0;
    for (int Dizin = 0; Dizin < öğe_BAĞ_DEĞ_SAY; Dizin++) {
        const int *원본 = (const int *)jkoros_syscall(3, Dizin, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        bağımsız_değişken_Liste[Dizin + 1] = bağımsız_değişken_Bellek + konum;
        for (int yuva_girdi = 0; yuva_girdi < 원본[0]; yuva_girdi++) {
            if (konum >= 2047) return 126;
            bağımsız_değişken_Bellek[konum++] = 원본[yuva_girdi + 1];
        }
        bağımsız_değişken_Bellek[konum++] = 0;
    }
    bağımsız_değişken_Liste[öğe_BAĞ_DEĞ_SAY + 1] = 0;
    return main(öğe_BAĞ_DEĞ_SAY + 1, bağımsız_değişken_Liste);
}
