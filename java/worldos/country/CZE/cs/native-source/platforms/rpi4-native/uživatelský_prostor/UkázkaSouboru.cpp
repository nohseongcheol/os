#include "Soubor_ABI.h"
#include "호출.h"
static int inicializátor_HODNOTA;
static volatile int inicializátor_přidat = 72;
static volatile double číslo_s_plovoucí_desetinnou_čárkou_přidat = 1.25;
static int 소멸횟수;
struct test_inicializace { test_inicializace() { inicializátor_HODNOTA = inicializátor_přidat + 1; } } 정적초기화;
class Automatická_Soubor {
    int INDEX;
public:
    explicit Automatická_Soubor(const char *Název) : INDEX(otevřít_Soubor(Název, pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600)) {}
    ~Automatická_Soubor() { if (INDEX >= 0) Zavřít_Soubor(INDEX); 소멸횟수++; }
    int popisovač_položka() const { return INDEX; }
};
extern "C" int START_uživatel_program(int) {
    if (inicializátor_HODNOTA != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double číslo_s_plovoucí_desetinnou_čárkou_HODNOTA = číslo_s_plovoucí_desetinnou_čárkou_přidat * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || číslo_s_plovoucí_desetinnou_čárkou_HODNOTA != 3.0) return 16;
    static const char Obsah_HODNOTA[] = "EL0 C++ → posix-kor → Java název_souboru · 안녕하세요 😀\n";
    char 읽은값[sizeof(Obsah_HODNOTA)] = {};
    {
        Automatická_Soubor název_souboru("uživatelský_prostor.txt");
        int INDEX = název_souboru.popisovač_položka();
        if (INDEX < 0 || zápis_Soubor_data(INDEX, Obsah_HODNOTA, sizeof(Obsah_HODNOTA)) != sizeof(Obsah_HODNOTA)) return 2;
        if (hledat_Soubor(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Obsah_HODNOTA); 순번++) if (읽은값[순번] != Obsah_HODNOTA[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (zápis_Soubor_data(1, Obsah_HODNOTA, sizeof(Obsah_HODNOTA) - 1) != sizeof(Obsah_HODNOTA) - 1) return 6;
    uintptr_t 바닥 = uživatel_Paměť_konec(0);
    if (바닥 != 0x02c00000 || uživatel_Paměť_konec(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Paměť_HODNOTA = (volatile unsigned char *)바닥;
    if (Paměť_HODNOTA[0] || Paměť_HODNOTA[8191]) return 8;
    Paměť_HODNOTA[8191] = 137;
    if (uživatel_Paměť_konec(바닥) != (intptr_t)바닥 || uživatel_Paměť_konec(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Paměť_HODNOTA[8191]) return 9;
    // 잘못된 uživatelský_prostor ukazatel/번호는 오류이며 커널을 중단하지 않는다.
    if (zápis_Soubor_data(1, (const void *)0x80000, 8) != -1 || číslo_chyby != 14) return 10;
    if (파일자료읽기(0, (void *)Obsah_HODNOTA, 1) != -1 || číslo_chyby != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Konec_program 시 열린 서술자가 자동 정리되어야 한다.
    if (otevřít_Soubor("uživatelský_prostor.txt", jen_pro_čtení_HODNOTA) < 0) return 15;
    return 0;
}
