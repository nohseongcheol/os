#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotek 없는 freestanding C++11 app_f5044b9b. 커널에 statisk_värde 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Innehåll_värde[] = "C++ → Java kärna_värde · 한글 😀";
    unsigned char läsa_värde[sizeof(Innehåll_värde)] = {};
    int filnamn = skapa_fil("tester.txt", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600);
    if (filnamn < 0) return 1;
    if (skriva_fil_data(filnamn, Innehåll_värde, sizeof(Innehåll_värde)) != sizeof(Innehåll_värde)) return 2;
    if (söka_fil(filnamn, 0, 처음기준) != 0) return 3;
    if (läsa_fil_data(filnamn, läsa_värde, sizeof(läsa_värde)) != sizeof(läsa_värde)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Innehåll_värde); 순번++) if (läsa_värde[순번] != (unsigned char)Innehåll_värde[순번]) return 5;
    if (läsa_fil_data(filnamn, läsa_värde, 1) != 0) return 6;
    if (incheckning_Files(filnamn) != -1 || felnummer != 38) return 7;
    if (Stäng_fil(filnamn) || Stäng_fil(filnamn) != -1 || felnummer != 9) return 8;
    filnamn = skapa_fil("tester.txt", skrivskyddad_värde);
    if (filnamn < 0 || skriva_fil_data(filnamn, Innehåll_värde, 1) != -1 || felnummer != 9) return 9;
    if (Stäng_fil(filnamn)) return 10;
    filnamn = skapa_fil("tester.txt", läsa_skriva | 끝에이어쓰기);
    if (filnamn < 0 || söka_fil(filnamn, 0, 처음기준) != 0 || skriva_fil_data(filnamn, "!", 1) != 1 || filstorlek(filnamn) != sizeof(Innehåll_värde) + 1) return 11;
    if (uppsättning_fil_längd(filnamn, 2) || söka_fil(filnamn, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (skriva_fil_data(filnamn, "x", 1) != 1 || filstorlek(filnamn) != 3 || Stäng_fil(filnamn)) return 13;
    filnamn = skapa_fil("구멍.bin", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600);
    if (filnamn < 0 || söka_fil(filnamn, 3, 처음기준) != 3 || skriva_fil_data(filnamn, "z", 1) != 1) return 14;
    if (söka_fil(filnamn, 0, 처음기준) != 0 || läsa_fil_data(filnamn, läsa_värde, 4) != 4 || läsa_värde[0] || läsa_värde[1] || läsa_värde[2] || läsa_värde[3] != 'z') return 15;
    if (ta_bort_fil_post_namn("구멍.bin") || filstorlek(filnamn) != 4 || Stäng_fil(filnamn)) return 16;
    if (skapa_fil("구멍.bin", skrivskyddad_värde) != -1 || felnummer != 2) return 17;
    if (skapa_fil("tester.txt", läsa_skriva | 새파일만들기, 0600) != -1 || felnummer != 17) return 18;
    if (skapa_fil("../금지", skrivskyddad_värde) != -1) return 19;
    return 0;
}
