#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotek 없는 freestanding C++11 app_f5044b9b. 커널에 statisk_VERDI 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Innhold_VERDI[] = "C++ → Java kjerne_VERDI · 한글 😀";
    unsigned char 읽은값[sizeof(Innhold_VERDI)] = {};
    int Fil = åpen_Fil("시험.txt", lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600);
    if (Fil < 0) return 1;
    if (skrive_Fil_data(Fil, Innhold_VERDI, sizeof(Innhold_VERDI)) != sizeof(Innhold_VERDI)) return 2;
    if (søk_Fil(Fil, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fil, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Innhold_VERDI); 순번++) if (읽은값[순번] != (unsigned char)Innhold_VERDI[순번]) return 5;
    if (파일자료읽기(Fil, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fil) != -1 || feilnummer != 38) return 7;
    if (Lukk_Fil(Fil) || Lukk_Fil(Fil) != -1 || feilnummer != 9) return 8;
    Fil = åpen_Fil("시험.txt", skrivebeskyttet_VERDI);
    if (Fil < 0 || skrive_Fil_data(Fil, Innhold_VERDI, 1) != -1 || feilnummer != 9) return 9;
    if (Lukk_Fil(Fil)) return 10;
    Fil = åpen_Fil("시험.txt", lese_og_skrive | 끝에이어쓰기);
    if (Fil < 0 || søk_Fil(Fil, 0, 처음기준) != 0 || skrive_Fil_data(Fil, "!", 1) != 1 || filstørrelse(Fil) != sizeof(Innhold_VERDI) + 1) return 11;
    if (sett_Fil_lengde(Fil, 2) || søk_Fil(Fil, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (skrive_Fil_data(Fil, "x", 1) != 1 || filstørrelse(Fil) != 3 || Lukk_Fil(Fil)) return 13;
    Fil = åpen_Fil("구멍.bin", lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600);
    if (Fil < 0 || søk_Fil(Fil, 3, 처음기준) != 3 || skrive_Fil_data(Fil, "z", 1) != 1) return 14;
    if (søk_Fil(Fil, 0, 처음기준) != 0 || 파일자료읽기(Fil, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (fjerne_Fil_oppføring_navn("구멍.bin") || filstørrelse(Fil) != 4 || Lukk_Fil(Fil)) return 16;
    if (åpen_Fil("구멍.bin", skrivebeskyttet_VERDI) != -1 || feilnummer != 2) return 17;
    if (åpen_Fil("시험.txt", lese_og_skrive | 새파일만들기, 0600) != -1 || feilnummer != 17) return 18;
    if (åpen_Fil("../금지", skrivebeskyttet_VERDI) != -1) return 19;
    return 0;
}
