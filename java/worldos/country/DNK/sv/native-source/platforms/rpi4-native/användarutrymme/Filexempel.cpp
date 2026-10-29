#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double flyttal_så = 1.25;
static int 소멸횟수;
struct test_initiering { test_initiering() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class automatisk_fil {
    int INDEX;
public:
    explicit automatisk_fil(const char *Namn) : INDEX(skapa_fil(Namn, läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600)) {}
    ~automatisk_fil() { if (INDEX >= 0) Stäng_fil(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int START_användare_app(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double flyttal_värde = flyttal_så * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || flyttal_värde != 3.0) return 16;
    static const char Innehåll_värde[] = "EL0 C++ → posix-kor → Java filnamn · 안녕하세요 😀\n";
    char läsa_värde[sizeof(Innehåll_värde)] = {};
    {
        automatisk_fil filnamn("användarutrymme.txt");
        int INDEX = filnamn.서술자();
        if (INDEX < 0 || skriva_fil_data(INDEX, Innehåll_värde, sizeof(Innehåll_värde)) != sizeof(Innehåll_värde)) return 2;
        if (söka_fil(INDEX, 0, 처음기준) || läsa_fil_data(INDEX, läsa_värde, sizeof(läsa_värde)) != sizeof(läsa_värde)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Innehåll_värde); 순번++) if (läsa_värde[순번] != Innehåll_värde[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (skriva_fil_data(1, Innehåll_värde, sizeof(Innehåll_värde) - 1) != sizeof(Innehåll_värde) - 1) return 6;
    uintptr_t 바닥 = användare_Minne_avsluta(0);
    if (바닥 != 0x02c00000 || användare_Minne_avsluta(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Minne_värde = (volatile unsigned char *)바닥;
    if (Minne_värde[0] || Minne_värde[8191]) return 8;
    Minne_värde[8191] = 137;
    if (användare_Minne_avsluta(바닥) != (intptr_t)바닥 || användare_Minne_avsluta(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Minne_värde[8191]) return 9;
    // 잘못된 användarutrymme markör/번호는 오류이며 커널을 중단하지 않는다.
    if (skriva_fil_data(1, (const void *)0x80000, 8) != -1 || felnummer != 14) return 10;
    if (läsa_fil_data(0, (void *)Innehåll_värde, 1) != -1 || felnummer != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), skärmbild_längd = 화면높이읽기();
    if (화면폭 <= 0 || skärmbild_längd <= 0 || 사용자호출(13, 화면폭-1, skärmbild_längd-1, 0, 2, 2, 0) != -22) return 13;
    if (skärmbild_rektangel(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Utgång_app 시 열린 서술자가 자동 정리되어야 한다.
    if (skapa_fil("användarutrymme.txt", skrivskyddad_värde) < 0) return 15;
    return 0;
}
