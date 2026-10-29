#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ knižnica 없는 freestanding C++11 program_f5044b9b. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char obsah_VALUE[] = "C++ → Java jadro_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(obsah_VALUE)] = {};
    int Súbor = otvoriť_Súbor("시험.txt", na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600);
    if (Súbor < 0) return 1;
    if (zapísať_Súbor_údaje(Súbor, obsah_VALUE, sizeof(obsah_VALUE)) != sizeof(obsah_VALUE)) return 2;
    if (hľadať_Súbor(Súbor, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Súbor, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(obsah_VALUE); 순번++) if (읽은값[순번] != (unsigned char)obsah_VALUE[순번]) return 5;
    if (파일자료읽기(Súbor, 읽은값, 1) != 0) return 6;
    if (potvrdenie_ukladací_priestor_súborov(Súbor) != -1 || chybové_číslo != 38) return 7;
    if (Zavrieť_Súbor(Súbor) || Zavrieť_Súbor(Súbor) != -1 || chybové_číslo != 9) return 8;
    Súbor = otvoriť_Súbor("시험.txt", iba_na_čítanie_VALUE);
    if (Súbor < 0 || zapísať_Súbor_údaje(Súbor, obsah_VALUE, 1) != -1 || chybové_číslo != 9) return 9;
    if (Zavrieť_Súbor(Súbor)) return 10;
    Súbor = otvoriť_Súbor("시험.txt", na_čítanie_a_zapisovanie | 끝에이어쓰기);
    if (Súbor < 0 || hľadať_Súbor(Súbor, 0, 처음기준) != 0 || zapísať_Súbor_údaje(Súbor, "!", 1) != 1 || veľkosť_súboru(Súbor) != sizeof(obsah_VALUE) + 1) return 11;
    if (množina_Súbor_dĺžka(Súbor, 2) || hľadať_Súbor(Súbor, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (zapísať_Súbor_údaje(Súbor, "x", 1) != 1 || veľkosť_súboru(Súbor) != 3 || Zavrieť_Súbor(Súbor)) return 13;
    Súbor = otvoriť_Súbor("구멍.bin", na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600);
    if (Súbor < 0 || hľadať_Súbor(Súbor, 3, 처음기준) != 3 || zapísať_Súbor_údaje(Súbor, "z", 1) != 1) return 14;
    if (hľadať_Súbor(Súbor, 0, 처음기준) != 0 || 파일자료읽기(Súbor, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (odobrať_Súbor_položka_názov("구멍.bin") || veľkosť_súboru(Súbor) != 4 || Zavrieť_Súbor(Súbor)) return 16;
    if (otvoriť_Súbor("구멍.bin", iba_na_čítanie_VALUE) != -1 || chybové_číslo != 2) return 17;
    if (otvoriť_Súbor("시험.txt", na_čítanie_a_zapisovanie | 새파일만들기, 0600) != -1 || chybové_číslo != 17) return 18;
    if (otvoriť_Súbor("../금지", iba_na_čítanie_VALUE) != -1) return 19;
    return 0;
}
