#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotek 없는 freestanding C++11 app_f5044b9b. 커널에 statisk_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Innhald_VALUE[] = "C++ → Java kjerne_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Innhald_VALUE)] = {};
    int Fil = opne_fil("시험.txt", lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600);
    if (Fil < 0) return 1;
    if (skrive_fil_data(Fil, Innhald_VALUE, sizeof(Innhald_VALUE)) != sizeof(Innhald_VALUE)) return 2;
    if (søk_fil(Fil, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fil, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Innhald_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Innhald_VALUE[순번]) return 5;
    if (파일자료읽기(Fil, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fil) != -1 || feilnummer != 38) return 7;
    if (Lukk_fil(Fil) || Lukk_fil(Fil) != -1 || feilnummer != 9) return 8;
    Fil = opne_fil("시험.txt", skriveverna_VALUE);
    if (Fil < 0 || skrive_fil_data(Fil, Innhald_VALUE, 1) != -1 || feilnummer != 9) return 9;
    if (Lukk_fil(Fil)) return 10;
    Fil = opne_fil("시험.txt", lese_og_skrivetilgang | 끝에이어쓰기);
    if (Fil < 0 || søk_fil(Fil, 0, 처음기준) != 0 || skrive_fil_data(Fil, "!", 1) != 1 || fil_endre_storleik(Fil) != sizeof(Innhald_VALUE) + 1) return 11;
    if (sett_fil_lengd(Fil, 2) || søk_fil(Fil, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (skrive_fil_data(Fil, "x", 1) != 1 || fil_endre_storleik(Fil) != 3 || Lukk_fil(Fil)) return 13;
    Fil = opne_fil("구멍.bin", lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600);
    if (Fil < 0 || søk_fil(Fil, 3, 처음기준) != 3 || skrive_fil_data(Fil, "z", 1) != 1) return 14;
    if (søk_fil(Fil, 0, 처음기준) != 0 || 파일자료읽기(Fil, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (fjerne_fil_oppføring_namn("구멍.bin") || fil_endre_storleik(Fil) != 4 || Lukk_fil(Fil)) return 16;
    if (opne_fil("구멍.bin", skriveverna_VALUE) != -1 || feilnummer != 2) return 17;
    if (opne_fil("시험.txt", lese_og_skrivetilgang | 새파일만들기, 0600) != -1 || feilnummer != 17) return 18;
    if (opne_fil("../금지", skriveverna_VALUE) != -1) return 19;
    return 0;
}
