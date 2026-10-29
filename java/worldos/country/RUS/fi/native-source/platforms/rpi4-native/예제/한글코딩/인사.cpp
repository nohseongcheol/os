#include "파일규약.h"
class viesti_Valvoja {
    int INDEKSI;
public:
    viesti_Valvoja(const char *Nimi) : INDEKSI(avata_Tiedosto(Nimi, luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600)) {}
    ~viesti_Valvoja() { if (INDEKSI >= 0) Sulje_Tiedosto(INDEKSI); }
    입출력결과형 Kirjoitus(const char *data, tavu_LASKE_TYYPPI Koko) { return kirjoitus_Tiedosto_data(INDEKSI, data, Koko); }
};
extern "C" int alku_käyttäjä_ohjelma(int argumentit) {
    (void)argumentit;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    viesti_Valvoja 문서("C++인사.txt");
    kirjoitus_Tiedosto_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Kirjoitus(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
