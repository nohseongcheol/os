#include "../명명/기계연결이름.h"
#include "Soubor_ABI.h"
// 표준 C++ knihovna 없는 freestanding C++11 program_f5044b9b. 커널에 statický_HODNOTA 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Obsah_HODNOTA[] = "C++ → Java jádro_HODNOTA · 한글 😀";
    unsigned char 읽은값[sizeof(Obsah_HODNOTA)] = {};
    int název_souboru = otevřít_Soubor("zkoušky.txt", pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600);
    if (název_souboru < 0) return 1;
    if (zápis_Soubor_data(název_souboru, Obsah_HODNOTA, sizeof(Obsah_HODNOTA)) != sizeof(Obsah_HODNOTA)) return 2;
    if (hledat_Soubor(název_souboru, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(název_souboru, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Obsah_HODNOTA); 순번++) if (읽은값[순번] != (unsigned char)Obsah_HODNOTA[순번]) return 5;
    if (파일자료읽기(název_souboru, 읽은값, 1) != 0) return 6;
    if (zápis_Files(název_souboru) != -1 || číslo_chyby != 38) return 7;
    if (Zavřít_Soubor(název_souboru) || Zavřít_Soubor(název_souboru) != -1 || číslo_chyby != 9) return 8;
    název_souboru = otevřít_Soubor("zkoušky.txt", jen_pro_čtení_HODNOTA);
    if (název_souboru < 0 || zápis_Soubor_data(název_souboru, Obsah_HODNOTA, 1) != -1 || číslo_chyby != 9) return 9;
    if (Zavřít_Soubor(název_souboru)) return 10;
    název_souboru = otevřít_Soubor("zkoušky.txt", pro_čtení_i_zápis | 끝에이어쓰기);
    if (název_souboru < 0 || hledat_Soubor(název_souboru, 0, 처음기준) != 0 || zápis_Soubor_data(název_souboru, "!", 1) != 1 || velikost_souboru(název_souboru) != sizeof(Obsah_HODNOTA) + 1) return 11;
    if (sada_Soubor_délka(název_souboru, 2) || hledat_Soubor(název_souboru, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (zápis_Soubor_data(název_souboru, "x", 1) != 1 || velikost_souboru(název_souboru) != 3 || Zavřít_Soubor(název_souboru)) return 13;
    název_souboru = otevřít_Soubor("구멍.bin", pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600);
    if (název_souboru < 0 || hledat_Soubor(název_souboru, 3, 처음기준) != 3 || zápis_Soubor_data(název_souboru, "z", 1) != 1) return 14;
    if (hledat_Soubor(název_souboru, 0, 처음기준) != 0 || 파일자료읽기(název_souboru, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (odebrat_Soubor_položka_název("구멍.bin") || velikost_souboru(název_souboru) != 4 || Zavřít_Soubor(název_souboru)) return 16;
    if (otevřít_Soubor("구멍.bin", jen_pro_čtení_HODNOTA) != -1 || číslo_chyby != 2) return 17;
    if (otevřít_Soubor("zkoušky.txt", pro_čtení_i_zápis | 새파일만들기, 0600) != -1 || číslo_chyby != 17) return 18;
    if (otevřít_Soubor("../금지", jen_pro_čtení_HODNOTA) != -1) return 19;
    return 0;
}
