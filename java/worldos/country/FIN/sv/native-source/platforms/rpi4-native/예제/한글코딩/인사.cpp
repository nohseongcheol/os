#include "파일규약.h"
class dokument_Ansvarig {
    int INDEX;
public:
    dokument_Ansvarig(const char *Namn) : INDEX(skapa_fil(Namn, läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600)) {}
    ~dokument_Ansvarig() { if (INDEX >= 0) Stäng_fil(INDEX); }
    입출력결과형 Skriv(const char *data, byte_ANTAL_Typ Storlek) { return skriva_fil_data(INDEX, data, Storlek); }
};
extern "C" int START_användare_app(int argument) {
    (void)argument;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_Ansvarig 문서("C++인사.txt");
    skriva_fil_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Skriv(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
