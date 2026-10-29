#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double mugikor_p_erein = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class automatiko_fitxategi {
    int INDIZE;
public:
    explicit automatiko_fitxategi(const char *Izena) : INDIZE(ireki_fitxategi(Izena, irakurri_idatzi | 없으면만들기 | 내용비우기, 0600)) {}
    ~automatiko_fitxategi() { if (INDIZE >= 0) itxi_fitxategi(INDIZE); 소멸횟수++; }
    int 서술자() const { return INDIZE; }
};
extern "C" int HASI_erabiltzaile_aplik(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double mugikor_p_balio = mugikor_p_erein * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || mugikor_p_balio != 3.0) return 16;
    static const char eduki_balio[] = "EL0 C++ → posix-kor → Java Fitxategia · 안녕하세요 😀\n";
    char 읽은값[sizeof(eduki_balio)] = {};
    {
        automatiko_fitxategi Fitxategia("erabiltzaile.txt");
        int INDIZE = Fitxategia.서술자();
        if (INDIZE < 0 || idatzi_fitxategi_datuak(INDIZE, eduki_balio, sizeof(eduki_balio)) != sizeof(eduki_balio)) return 2;
        if (bilatu_fitxategi(INDIZE, 0, 처음기준) || 파일자료읽기(INDIZE, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(eduki_balio); 순번++) if (읽은값[순번] != eduki_balio[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (idatzi_fitxategi_datuak(1, eduki_balio, sizeof(eduki_balio) - 1) != sizeof(eduki_balio) - 1) return 6;
    uintptr_t 바닥 = erabiltzaile_Memoria_amaitu(0);
    if (바닥 != 0x02c00000 || erabiltzaile_Memoria_amaitu(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memoria_balio = (volatile unsigned char *)바닥;
    if (Memoria_balio[0] || Memoria_balio[8191]) return 8;
    Memoria_balio[8191] = 137;
    if (erabiltzaile_Memoria_amaitu(바닥) != (intptr_t)바닥 || erabiltzaile_Memoria_amaitu(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memoria_balio[8191]) return 9;
    // 잘못된 erabiltzaile erakusle/번호는 오류이며 커널을 중단하지 않는다.
    if (idatzi_fitxategi_datuak(1, (const void *)0x80000, 8) != -1 || errorearen_zenbaki != 14) return 10;
    if (파일자료읽기(0, (void *)eduki_balio, 1) != -1 || errorearen_zenbaki != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 irten_aplik 시 열린 서술자가 자동 정리되어야 한다.
    if (ireki_fitxategi("erabiltzaile.txt", irakurtzeko_soilik_balio) < 0) return 15;
    return 0;
}
