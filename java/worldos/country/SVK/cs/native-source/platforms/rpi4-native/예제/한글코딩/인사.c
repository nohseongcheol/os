#include "Soubor_ABI.h"
int START_uživatel_program(int argumenty) {
    (void)argumenty;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = otevřít_Soubor("C인사.txt", pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = zápis_Soubor_data(문서, 인사말, sizeof(인사말) - 1);
    Zavřít_Soubor(문서);
    zápis_Soubor_data(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
