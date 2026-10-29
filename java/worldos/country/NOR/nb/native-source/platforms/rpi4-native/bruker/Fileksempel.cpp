#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double flyttall_så = 1.25;
static int 소멸횟수;
struct test_initialisering { test_initialisering() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automatisk_Fil {
    int INDEKS;
public:
    explicit Automatisk_Fil(const char *Navn) : INDEKS(åpen_Fil(Navn, lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600)) {}
    ~Automatisk_Fil() { if (INDEKS >= 0) Lukk_Fil(INDEKS); 소멸횟수++; }
    int 서술자() const { return INDEKS; }
};
extern "C" int START_bruker_app(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double flyttall_VERDI = flyttall_så * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || flyttall_VERDI != 3.0) return 16;
    static const char Innhold_VERDI[] = "EL0 C++ → posix-kor → Java Fil · 안녕하세요 😀\n";
    char 읽은값[sizeof(Innhold_VERDI)] = {};
    {
        Automatisk_Fil Fil("bruker.txt");
        int INDEKS = Fil.서술자();
        if (INDEKS < 0 || skrive_Fil_data(INDEKS, Innhold_VERDI, sizeof(Innhold_VERDI)) != sizeof(Innhold_VERDI)) return 2;
        if (søk_Fil(INDEKS, 0, 처음기준) || 파일자료읽기(INDEKS, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Innhold_VERDI); 순번++) if (읽은값[순번] != Innhold_VERDI[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (skrive_Fil_data(1, Innhold_VERDI, sizeof(Innhold_VERDI) - 1) != sizeof(Innhold_VERDI) - 1) return 6;
    uintptr_t 바닥 = bruker_Minne_avslutte_en_samtale(0);
    if (바닥 != 0x02c00000 || bruker_Minne_avslutte_en_samtale(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Minne_VERDI = (volatile unsigned char *)바닥;
    if (Minne_VERDI[0] || Minne_VERDI[8191]) return 8;
    Minne_VERDI[8191] = 137;
    if (bruker_Minne_avslutte_en_samtale(바닥) != (intptr_t)바닥 || bruker_Minne_avslutte_en_samtale(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Minne_VERDI[8191]) return 9;
    // 잘못된 bruker peker/번호는 오류이며 커널을 중단하지 않는다.
    if (skrive_Fil_data(1, (const void *)0x80000, 8) != -1 || feilnummer != 14) return 10;
    if (파일자료읽기(0, (void *)Innhold_VERDI, 1) != -1 || feilnummer != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), skjermbilde_lengde = 화면높이읽기();
    if (화면폭 <= 0 || skjermbilde_lengde <= 0 || 사용자호출(13, 화면폭-1, skjermbilde_lengde-1, 0, 2, 2, 0) != -22) return 13;
    if (skjermbilde_rektangel(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Utgang_app 시 열린 서술자가 자동 정리되어야 한다.
    if (åpen_Fil("bruker.txt", skrivebeskyttet_VERDI) < 0) return 15;
    return 0;
}
