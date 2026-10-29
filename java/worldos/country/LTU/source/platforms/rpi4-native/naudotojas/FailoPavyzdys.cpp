#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double slankiojantis_p_pirminė_reikšmė = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automatinė_Failas {
    int INDEX;
public:
    explicit Automatinė_Failas(const char *Pavadinimas_2) : INDEX(kurti_Failas(Pavadinimas_2, 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600)) {}
    ~Automatinė_Failas() { if (INDEX >= 0) Uždaryti_Failas(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Start_naudotojas_programa(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double slankiojantis_p_VALUE = slankiojantis_p_pirminė_reikšmė * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || slankiojantis_p_VALUE != 3.0) return 16;
    static const char Turinys_VALUE[] = "EL0 C++ → posix-kor → Java Failas · 안녕하세요 😀\n";
    char 읽은값[sizeof(Turinys_VALUE)] = {};
    {
        Automatinė_Failas Failas("naudotojas.txt");
        int INDEX = Failas.서술자();
        if (INDEX < 0 || rašymas_Failas_duomenys(INDEX, Turinys_VALUE, sizeof(Turinys_VALUE)) != sizeof(Turinys_VALUE)) return 2;
        if (ieškoti_Failas(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Turinys_VALUE); 순번++) if (읽은값[순번] != Turinys_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (rašymas_Failas_duomenys(1, Turinys_VALUE, sizeof(Turinys_VALUE) - 1) != sizeof(Turinys_VALUE) - 1) return 6;
    uintptr_t 바닥 = naudotojas_atmintis_baigti_pokalbį(0);
    if (바닥 != 0x02c00000 || naudotojas_atmintis_baigti_pokalbį(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *atmintis_VALUE = (volatile unsigned char *)바닥;
    if (atmintis_VALUE[0] || atmintis_VALUE[8191]) return 8;
    atmintis_VALUE[8191] = 137;
    if (naudotojas_atmintis_baigti_pokalbį(바닥) != (intptr_t)바닥 || naudotojas_atmintis_baigti_pokalbį(바닥 + 8192) != (intptr_t)(바닥 + 8192) || atmintis_VALUE[8191]) return 9;
    // 잘못된 naudotojas rodyklė/번호는 오류이며 커널을 중단하지 않는다.
    if (rašymas_Failas_duomenys(1, (const void *)0x80000, 8) != -1 || klaidos_numeris != 14) return 10;
    if (파일자료읽기(0, (void *)Turinys_VALUE, 1) != -1 || klaidos_numeris != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Baigti_programa_086bb533 시 열린 서술자가 자동 정리되어야 한다.
    if (kurti_Failas("naudotojas.txt", tik_skaitomas_VALUE) < 0) return 15;
    return 0;
}
