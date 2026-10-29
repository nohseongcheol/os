#include "파일규약.h"
class dokument_Upravitelj {
    int INDEX;
public:
    dokument_Upravitelj(const char *Ime) : INDEX(odprto_Datoteka(Ime, branje_pisanje | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_Upravitelj() { if (INDEX >= 0) Zapri_Datoteka(INDEX); }
    입출력결과형 Pisanje(const char *podatki, bajt_COUNT_Tip Velikost) { return pisati_Datoteka_podatki(INDEX, podatki, Velikost); }
};
extern "C" int Start_uporabnik_aplikacija(int Argumenti) {
    (void)Argumenti;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_Upravitelj 문서("C++인사.txt");
    pisati_Datoteka_podatki(1, 인사말, sizeof(인사말) - 1);
    return 문서.Pisanje(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
