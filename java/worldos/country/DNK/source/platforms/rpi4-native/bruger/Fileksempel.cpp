#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double flydende_tal_så = 1.25;
static int 소멸횟수;
struct test_initialisering { test_initialisering() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automatisk_fil {
    int INDEKS;
public:
    explicit Automatisk_fil(const char *Navn) : INDEKS(åben_fil(Navn, læse_skrive | 없으면만들기 | afkorte_Indhold, 0600)) {}
    ~Automatisk_fil() { if (INDEKS >= 0) Luk_fil(INDEKS); 소멸횟수++; }
    int 서술자() const { return INDEKS; }
};
extern "C" int START_bruger_app(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double flydende_tal_VÆRDI = flydende_tal_så * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || flydende_tal_VÆRDI != 3.0) return 16;
    static const char Indhold_VÆRDI[] = "EL0 C++ → posix-kor → Java Fil · 안녕하세요 😀\n";
    char 읽은값[sizeof(Indhold_VÆRDI)] = {};
    {
        Automatisk_fil Fil("bruger.txt");
        int INDEKS = Fil.서술자();
        if (INDEKS < 0 || skrive_fil_data(INDEKS, Indhold_VÆRDI, sizeof(Indhold_VÆRDI)) != sizeof(Indhold_VÆRDI)) return 2;
        if (søge_fil(INDEKS, 0, 처음기준) || 파일자료읽기(INDEKS, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Indhold_VÆRDI); 순번++) if (읽은값[순번] != Indhold_VÆRDI[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (skrive_fil_data(1, Indhold_VÆRDI, sizeof(Indhold_VÆRDI) - 1) != sizeof(Indhold_VÆRDI) - 1) return 6;
    uintptr_t 바닥 = bruger_Hukommelse_afslutte_et_opkald(0);
    if (바닥 != 0x02c00000 || bruger_Hukommelse_afslutte_et_opkald(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Hukommelse_VÆRDI = (volatile unsigned char *)바닥;
    if (Hukommelse_VÆRDI[0] || Hukommelse_VÆRDI[8191]) return 8;
    Hukommelse_VÆRDI[8191] = 137;
    if (bruger_Hukommelse_afslutte_et_opkald(바닥) != (intptr_t)바닥 || bruger_Hukommelse_afslutte_et_opkald(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Hukommelse_VÆRDI[8191]) return 9;
    // 잘못된 bruger markør/번호는 오류이며 커널을 중단하지 않는다.
    if (skrive_fil_data(1, (const void *)0x80000, 8) != -1 || fejlnummer != 14) return 10;
    if (파일자료읽기(0, (void *)Indhold_VÆRDI, 1) != -1 || fejlnummer != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), skærmbillede_varighed = 화면높이읽기();
    if (화면폭 <= 0 || skærmbillede_varighed <= 0 || 사용자호출(13, 화면폭-1, skærmbillede_varighed-1, 0, 2, 2, 0) != -22) return 13;
    if (skærmbillede_rektangel(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Afslut_app 시 열린 서술자가 자동 정리되어야 한다.
    if (åben_fil("bruger.txt", skrivebeskyttet_VÆRDI) < 0) return 15;
    return 0;
}
