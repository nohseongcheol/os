#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double drijvende_komma_seed = 1.25;
static int 소멸횟수;
struct test_initialisatie { test_initialisatie() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automatisch_Bestand {
    int INDEX;
public:
    explicit Automatisch_Bestand(const char *Naam) : INDEX(open_Bestand(Naam, lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600)) {}
    ~Automatisch_Bestand() { if (INDEX >= 0) Sluiten_Bestand(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int START_gebruiker_app(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double drijvende_komma_WAARDE = drijvende_komma_seed * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || drijvende_komma_WAARDE != 3.0) return 16;
    static const char Inhoud_WAARDE[] = "EL0 C++ → posix-kor → Java bestand · 안녕하세요 😀\n";
    char 읽은값[sizeof(Inhoud_WAARDE)] = {};
    {
        Automatisch_Bestand bestand("gebruikersruimte.txt");
        int INDEX = bestand.서술자();
        if (INDEX < 0 || schrijven_Bestand_gegevens(INDEX, Inhoud_WAARDE, sizeof(Inhoud_WAARDE)) != sizeof(Inhoud_WAARDE)) return 2;
        if (zoeken_Bestand(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Inhoud_WAARDE); 순번++) if (읽은값[순번] != Inhoud_WAARDE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (schrijven_Bestand_gegevens(1, Inhoud_WAARDE, sizeof(Inhoud_WAARDE) - 1) != sizeof(Inhoud_WAARDE) - 1) return 6;
    uintptr_t 바닥 = gebruiker_Geheugen_beëindigen(0);
    if (바닥 != 0x02c00000 || gebruiker_Geheugen_beëindigen(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Geheugen_WAARDE = (volatile unsigned char *)바닥;
    if (Geheugen_WAARDE[0] || Geheugen_WAARDE[8191]) return 8;
    Geheugen_WAARDE[8191] = 137;
    if (gebruiker_Geheugen_beëindigen(바닥) != (intptr_t)바닥 || gebruiker_Geheugen_beëindigen(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Geheugen_WAARDE[8191]) return 9;
    // 잘못된 gebruikersruimte wijzer/번호는 오류이며 커널을 중단하지 않는다.
    if (schrijven_Bestand_gegevens(1, (const void *)0x80000, 8) != -1 || foutnummer != 14) return 10;
    if (파일자료읽기(0, (void *)Inhoud_WAARDE, 1) != -1 || foutnummer != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), scherm_tijdsduur = 화면높이읽기();
    if (화면폭 <= 0 || scherm_tijdsduur <= 0 || 사용자호출(13, 화면폭-1, scherm_tijdsduur-1, 0, 2, 2, 0) != -22) return 13;
    if (scherm_rechthoek(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Einde_app 시 열린 서술자가 자동 정리되어야 한다.
    if (open_Bestand("gebruikersruimte.txt", alleen_lezen_WAARDE) < 0) return 15;
    return 0;
}
