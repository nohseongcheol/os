#include "Soubor_ABI.h"
class zpráva_Správce {
    int INDEX;
public:
    zpráva_Správce(const char *Název) : INDEX(otevřít_Soubor(Název, pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600)) {}
    ~zpráva_Správce() { if (INDEX >= 0) Zavřít_Soubor(INDEX); }
    입출력결과형 Zápis(const char *data, bajt_POČET_TYP Velikost) { return zápis_Soubor_data(INDEX, data, Velikost); }
};
extern "C" int START_uživatel_program(int argumenty) {
    (void)argumenty;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    zpráva_Správce 문서("C++인사.txt");
    zápis_Soubor_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Zápis(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
