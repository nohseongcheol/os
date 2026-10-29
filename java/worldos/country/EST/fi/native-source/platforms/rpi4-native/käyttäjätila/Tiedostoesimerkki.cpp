#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double liukuluku_alustaa = 1.25;
static int 소멸횟수;
struct testi_valmistelu { testi_valmistelu() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automaattinen_Tiedosto {
    int INDEKSI;
public:
    explicit Automaattinen_Tiedosto(const char *Nimi) : INDEKSI(avata_Tiedosto(Nimi, luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600)) {}
    ~Automaattinen_Tiedosto() { if (INDEKSI >= 0) Sulje_Tiedosto(INDEKSI); 소멸횟수++; }
    int 서술자() const { return INDEKSI; }
};
extern "C" int alku_käyttäjä_ohjelma(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double liukuluku_ARVO = liukuluku_alustaa * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || liukuluku_ARVO != 3.0) return 16;
    static const char Sisältö_ARVO[] = "EL0 C++ → posix-kor → Java tiedoston_nimi · 안녕하세요 😀\n";
    char lukea_ARVO[sizeof(Sisältö_ARVO)] = {};
    {
        Automaattinen_Tiedosto tiedoston_nimi("käyttäjätila.txt");
        int INDEKSI = tiedoston_nimi.서술자();
        if (INDEKSI < 0 || kirjoitus_Tiedosto_data(INDEKSI, Sisältö_ARVO, sizeof(Sisältö_ARVO)) != sizeof(Sisältö_ARVO)) return 2;
        if (hae_Tiedosto(INDEKSI, 0, 처음기준) || lukea_Tiedosto_data(INDEKSI, lukea_ARVO, sizeof(lukea_ARVO)) != sizeof(lukea_ARVO)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Sisältö_ARVO); 순번++) if (lukea_ARVO[순번] != Sisältö_ARVO[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (kirjoitus_Tiedosto_data(1, Sisältö_ARVO, sizeof(Sisältö_ARVO) - 1) != sizeof(Sisältö_ARVO) - 1) return 6;
    uintptr_t 바닥 = käyttäjä_Muisti_lopettaa_puhelu(0);
    if (바닥 != 0x02c00000 || käyttäjä_Muisti_lopettaa_puhelu(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Muisti_ARVO = (volatile unsigned char *)바닥;
    if (Muisti_ARVO[0] || Muisti_ARVO[8191]) return 8;
    Muisti_ARVO[8191] = 137;
    if (käyttäjä_Muisti_lopettaa_puhelu(바닥) != (intptr_t)바닥 || käyttäjä_Muisti_lopettaa_puhelu(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Muisti_ARVO[8191]) return 9;
    // 잘못된 käyttäjätila osoitin/번호는 오류이며 커널을 중단하지 않는다.
    if (kirjoitus_Tiedosto_data(1, (const void *)0x80000, 8) != -1 || virhenumero != 14) return 10;
    if (lukea_Tiedosto_data(0, (void *)Sisältö_ARVO, 1) != -1 || virhenumero != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Lopeta_ohjelma 시 열린 서술자가 자동 정리되어야 한다.
    if (avata_Tiedosto("käyttäjätila.txt", vain_luku_ARVO) < 0) return 15;
    return 0;
}
