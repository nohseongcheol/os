#include "파일규약.h"
class dokument_Upravitelj {
    int INDEX;
public:
    dokument_Upravitelj(const char *Ime) : INDEX(otvoreno_Datoteka(Ime, 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600)) {}
    ~dokument_Upravitelj() { if (INDEX >= 0) Zatvori_Datoteka(INDEX); }
    입출력결과형 Zapisuj(const char *podaci, bajt_COUNT_TYPE Veličina) { return zapisivanje_Datoteka_podaci(INDEX, podaci, Veličina); }
};
extern "C" int START_korisnik_program(int Argumenti) {
    (void)Argumenti;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_Upravitelj 문서("C++인사.txt");
    zapisivanje_Datoteka_podaci(1, 인사말, sizeof(인사말) - 1);
    return 문서.Zapisuj(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
