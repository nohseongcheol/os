#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double lebegőpontos_szám_beültet = 1.25;
static int 소멸횟수;
struct teszt_inicializálás { teszt_inicializálás() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automatikus_Fájl {
    int INDEX;
public:
    explicit Automatikus_Fájl(const char *Név) : INDEX(készít_Fájl(Név, 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600)) {}
    ~Automatikus_Fájl() { if (INDEX >= 0) bezár_Fájl(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int START_felhasználó_app(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double lebegőpontos_szám_ÉRTÉK = lebegőpontos_szám_beültet * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || lebegőpontos_szám_ÉRTÉK != 3.0) return 16;
    static const char Tartalom_ÉRTÉK[] = "EL0 C++ → posix-kor → Java Fájl · 안녕하세요 😀\n";
    char 읽은값[sizeof(Tartalom_ÉRTÉK)] = {};
    {
        Automatikus_Fájl Fájl("felhasználó.txt");
        int INDEX = Fájl.서술자();
        if (INDEX < 0 || ír_Fájl_adat(INDEX, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK)) != sizeof(Tartalom_ÉRTÉK)) return 2;
        if (keres_Fájl(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Tartalom_ÉRTÉK); 순번++) if (읽은값[순번] != Tartalom_ÉRTÉK[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (ír_Fájl_adat(1, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK) - 1) != sizeof(Tartalom_ÉRTÉK) - 1) return 6;
    uintptr_t 바닥 = felhasználó_Memória_megszüntet(0);
    if (바닥 != 0x02c00000 || felhasználó_Memória_megszüntet(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memória_ÉRTÉK = (volatile unsigned char *)바닥;
    if (Memória_ÉRTÉK[0] || Memória_ÉRTÉK[8191]) return 8;
    Memória_ÉRTÉK[8191] = 137;
    if (felhasználó_Memória_megszüntet(바닥) != (intptr_t)바닥 || felhasználó_Memória_megszüntet(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memória_ÉRTÉK[8191]) return 9;
    // 잘못된 felhasználó mutató/번호는 오류이며 커널을 중단하지 않는다.
    if (ír_Fájl_adat(1, (const void *)0x80000, 8) != -1 || hibaszám != 14) return 10;
    if (파일자료읽기(0, (void *)Tartalom_ÉRTÉK, 1) != -1 || hibaszám != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 kilép_app 시 열린 서술자가 자동 정리되어야 한다.
    if (készít_Fájl("felhasználó.txt", írásvédett_ÉRTÉK) < 0) return 15;
    return 0;
}
