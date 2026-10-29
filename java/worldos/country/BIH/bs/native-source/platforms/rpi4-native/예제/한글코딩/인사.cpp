#include "파일규약.h"
class dokument_menadžer {
    int INDEX;
public:
    dokument_menadžer(const char *Naziv) : INDEX(kreirati_fajl(Naziv, i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_menadžer() { if (INDEX >= 0) zatvoriti_fajl(INDEX); }
    입출력결과형 Piši(const char *podaci, bajt_COUNT_TYPE Veličina) { return pisati_fajl_podaci(INDEX, podaci, Veličina); }
};
extern "C" int START_korisnik_program(int Argumenti) {
    (void)Argumenti;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_menadžer 문서("C++인사.txt");
    pisati_fajl_podaci(1, 인사말, sizeof(인사말) - 1);
    return 문서.Piši(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
