#include "파일규약.h"
class melding_overordnet {
    int INDEKS;
public:
    melding_overordnet(const char *Navn) : INDEKS(åpen_Fil(Navn, lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600)) {}
    ~melding_overordnet() { if (INDEKS >= 0) Lukk_Fil(INDEKS); }
    입출력결과형 Skriv(const char *data, byte_ANTALL_Type Størrelse) { return skrive_Fil_data(INDEKS, data, Størrelse); }
};
extern "C" int START_bruker_app(int Argumenter) {
    (void)Argumenter;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    melding_overordnet 문서("C++인사.txt");
    skrive_Fil_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Skriv(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
