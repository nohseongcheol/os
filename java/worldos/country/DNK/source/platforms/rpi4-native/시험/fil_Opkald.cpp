#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotek 없는 freestanding C++11 app_f5044b9b. 커널에 statisk_VÆRDI 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Indhold_VÆRDI[] = "C++ → Java kerne_VÆRDI · 한글 😀";
    unsigned char 읽은값[sizeof(Indhold_VÆRDI)] = {};
    int Fil = åben_fil("시험.txt", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600);
    if (Fil < 0) return 1;
    if (skrive_fil_data(Fil, Indhold_VÆRDI, sizeof(Indhold_VÆRDI)) != sizeof(Indhold_VÆRDI)) return 2;
    if (søge_fil(Fil, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fil, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Indhold_VÆRDI); 순번++) if (읽은값[순번] != (unsigned char)Indhold_VÆRDI[순번]) return 5;
    if (파일자료읽기(Fil, 읽은값, 1) != 0) return 6;
    if (udføre_Files(Fil) != -1 || fejlnummer != 38) return 7;
    if (Luk_fil(Fil) || Luk_fil(Fil) != -1 || fejlnummer != 9) return 8;
    Fil = åben_fil("시험.txt", skrivebeskyttet_VÆRDI);
    if (Fil < 0 || skrive_fil_data(Fil, Indhold_VÆRDI, 1) != -1 || fejlnummer != 9) return 9;
    if (Luk_fil(Fil)) return 10;
    Fil = åben_fil("시험.txt", læse_skrive | 끝에이어쓰기);
    if (Fil < 0 || søge_fil(Fil, 0, 처음기준) != 0 || skrive_fil_data(Fil, "!", 1) != 1 || filstørrelse(Fil) != sizeof(Indhold_VÆRDI) + 1) return 11;
    if (sæt_fil_varighed(Fil, 2) || søge_fil(Fil, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (skrive_fil_data(Fil, "x", 1) != 1 || filstørrelse(Fil) != 3 || Luk_fil(Fil)) return 13;
    Fil = åben_fil("구멍.bin", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600);
    if (Fil < 0 || søge_fil(Fil, 3, 처음기준) != 3 || skrive_fil_data(Fil, "z", 1) != 1) return 14;
    if (søge_fil(Fil, 0, 처음기준) != 0 || 파일자료읽기(Fil, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (fjerne_fil_post_navn("구멍.bin") || filstørrelse(Fil) != 4 || Luk_fil(Fil)) return 16;
    if (åben_fil("구멍.bin", skrivebeskyttet_VÆRDI) != -1 || fejlnummer != 2) return 17;
    if (åben_fil("시험.txt", læse_skrive | 새파일만들기, 0600) != -1 || fejlnummer != 17) return 18;
    if (åben_fil("../금지", skrivebeskyttet_VÆRDI) != -1) return 19;
    return 0;
}
