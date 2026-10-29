#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double plavajoče_p_seme = 1.25;
static int 소멸횟수;
struct preskusiti_inicializacija { preskusiti_inicializacija() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Samodejno_Datoteka {
    int INDEX;
public:
    explicit Samodejno_Datoteka(const char *Ime) : INDEX(odprto_Datoteka(Ime, branje_pisanje | 없으면만들기 | 내용비우기, 0600)) {}
    ~Samodejno_Datoteka() { if (INDEX >= 0) Zapri_Datoteka(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Start_uporabnik_aplikacija(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double plavajoče_p_VALUE = plavajoče_p_seme * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || plavajoče_p_VALUE != 3.0) return 16;
    static const char vsebina_VALUE[] = "EL0 C++ → posix-kor → Java Datoteka · 안녕하세요 😀\n";
    char 읽은값[sizeof(vsebina_VALUE)] = {};
    {
        Samodejno_Datoteka Datoteka("uporabnik.txt");
        int INDEX = Datoteka.서술자();
        if (INDEX < 0 || pisati_Datoteka_podatki(INDEX, vsebina_VALUE, sizeof(vsebina_VALUE)) != sizeof(vsebina_VALUE)) return 2;
        if (iskati_Datoteka(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(vsebina_VALUE); 순번++) if (읽은값[순번] != vsebina_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (pisati_Datoteka_podatki(1, vsebina_VALUE, sizeof(vsebina_VALUE) - 1) != sizeof(vsebina_VALUE) - 1) return 6;
    uintptr_t 바닥 = uporabnik_pomnilnik_končati_klic(0);
    if (바닥 != 0x02c00000 || uporabnik_pomnilnik_končati_klic(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *pomnilnik_VALUE = (volatile unsigned char *)바닥;
    if (pomnilnik_VALUE[0] || pomnilnik_VALUE[8191]) return 8;
    pomnilnik_VALUE[8191] = 137;
    if (uporabnik_pomnilnik_končati_klic(바닥) != (intptr_t)바닥 || uporabnik_pomnilnik_končati_klic(바닥 + 8192) != (intptr_t)(바닥 + 8192) || pomnilnik_VALUE[8191]) return 9;
    // 잘못된 uporabnik kazalec/번호는 오류이며 커널을 중단하지 않는다.
    if (pisati_Datoteka_podatki(1, (const void *)0x80000, 8) != -1 || številka_napake != 14) return 10;
    if (파일자료읽기(0, (void *)vsebina_VALUE, 1) != -1 || številka_napake != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Izhod_aplikacija 시 열린 서술자가 자동 정리되어야 한다.
    if (odprto_Datoteka("uporabnik.txt", samo_za_branje_VALUE) < 0) return 15;
    return 0;
}
