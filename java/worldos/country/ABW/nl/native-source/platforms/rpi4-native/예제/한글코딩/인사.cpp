#include "파일규약.h"
class bericht_Manager {
    int INDEX;
public:
    bericht_Manager(const char *Naam) : INDEX(open_Bestand(Naam, lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600)) {}
    ~bericht_Manager() { if (INDEX >= 0) Sluiten_Bestand(INDEX); }
    입출력결과형 Schrijven(const char *gegevens, byte_AANTAL_TYPE Grootte) { return schrijven_Bestand_gegevens(INDEX, gegevens, Grootte); }
};
extern "C" int START_gebruiker_app(int argumenten) {
    (void)argumenten;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    bericht_Manager Guides("C++인사.txt");
    schrijven_Bestand_gegevens(1, 인사말, sizeof(인사말) - 1);
    return Guides.Schrijven(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
