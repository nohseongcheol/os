#include "파일규약.h"
class bilag_Leder {
    int INDEKS;
public:
    bilag_Leder(const char *Navn) : INDEKS(åben_fil(Navn, læse_skrive | 없으면만들기 | afkorte_Indhold, 0600)) {}
    ~bilag_Leder() { if (INDEKS >= 0) Luk_fil(INDEKS); }
    입출력결과형 Skrive(const char *data, byte_TÆL_Type Størrelse) { return skrive_fil_data(INDEKS, data, Størrelse); }
};
extern "C" int START_bruger_app(int Argumenter) {
    (void)Argumenter;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    bilag_Leder 문서("C++인사.txt");
    skrive_fil_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Skrive(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
