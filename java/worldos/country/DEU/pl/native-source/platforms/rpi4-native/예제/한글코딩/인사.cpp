#include "Plik_ABI.h"
class dokument_Menedżer {
    int INDEKS;
public:
    dokument_Menedżer(const char *Nazwa) : INDEKS(otwarty_Plik(Nazwa, R_W | 없으면만들기 | obcinać_Spis_treści, 0600)) {}
    ~dokument_Menedżer() { if (INDEKS >= 0) Zamknij_Plik(INDEKS); }
    입출력결과형 Zapis(const char *dane, bajt_ILE_LICZB_TYP Rozmiar) { return zapis_Plik_dane(INDEKS, dane, Rozmiar); }
};
extern "C" int START_użytkownik_program(int argumenty) {
    (void)argumenty;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_Menedżer 문서("C++인사.txt");
    zapis_Plik_dane(1, 인사말, sizeof(인사말) - 1);
    return 문서.Zapis(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
