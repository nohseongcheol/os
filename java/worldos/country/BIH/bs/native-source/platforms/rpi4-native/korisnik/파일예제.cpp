#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double plutajuće_p_dodavanje_baze_podataka = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automatski_fajl {
    int INDEX;
public:
    explicit Automatski_fajl(const char *Naziv) : INDEX(kreirati_fajl(Naziv, i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600)) {}
    ~Automatski_fajl() { if (INDEX >= 0) zatvoriti_fajl(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int START_korisnik_program(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double plutajuće_p_VALUE = plutajuće_p_dodavanje_baze_podataka * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || plutajuće_p_VALUE != 3.0) return 16;
    static const char Sadržaj_VALUE[] = "EL0 C++ → posix-kor → Java Fajl · 안녕하세요 😀\n";
    char 읽은값[sizeof(Sadržaj_VALUE)] = {};
    {
        Automatski_fajl Fajl("korisnik.txt");
        int INDEX = Fajl.서술자();
        if (INDEX < 0 || pisati_fajl_podaci(INDEX, Sadržaj_VALUE, sizeof(Sadržaj_VALUE)) != sizeof(Sadržaj_VALUE)) return 2;
        if (tražiti_fajl(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Sadržaj_VALUE); 순번++) if (읽은값[순번] != Sadržaj_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (pisati_fajl_podaci(1, Sadržaj_VALUE, sizeof(Sadržaj_VALUE) - 1) != sizeof(Sadržaj_VALUE) - 1) return 6;
    uintptr_t 바닥 = korisnik_Memorija_završiti(0);
    if (바닥 != 0x02c00000 || korisnik_Memorija_završiti(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memorija_VALUE = (volatile unsigned char *)바닥;
    if (Memorija_VALUE[0] || Memorija_VALUE[8191]) return 8;
    Memorija_VALUE[8191] = 137;
    if (korisnik_Memorija_završiti(바닥) != (intptr_t)바닥 || korisnik_Memorija_završiti(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memorija_VALUE[8191]) return 9;
    // 잘못된 korisnik pokazivač/번호는 오류이며 커널을 중단하지 않는다.
    if (pisati_fajl_podaci(1, (const void *)0x80000, 8) != -1 || broj_greške != 14) return 10;
    if (파일자료읽기(0, (void *)Sadržaj_VALUE, 1) != -1 || broj_greške != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 izaći_program 시 열린 서술자가 자동 정리되어야 한다.
    if (kreirati_fajl("korisnik.txt", samo_za_čitanje_VALUE) < 0) return 15;
    return 0;
}
