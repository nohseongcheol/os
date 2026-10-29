#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotheek 없는 freestanding C++11 app_f5044b9b. 커널에 statisch_WAARDE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Inhoud_WAARDE[] = "C++ → Java kernel_WAARDE · 한글 😀";
    unsigned char 읽은값[sizeof(Inhoud_WAARDE)] = {};
    int bestand = open_Bestand("tests.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (bestand < 0) return 1;
    if (schrijven_Bestand_gegevens(bestand, Inhoud_WAARDE, sizeof(Inhoud_WAARDE)) != sizeof(Inhoud_WAARDE)) return 2;
    if (zoeken_Bestand(bestand, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(bestand, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Inhoud_WAARDE); 순번++) if (읽은값[순번] != (unsigned char)Inhoud_WAARDE[순번]) return 5;
    if (파일자료읽기(bestand, 읽은값, 1) != 0) return 6;
    if (doorvoeren_Files(bestand) != -1 || foutnummer != 38) return 7;
    if (Sluiten_Bestand(bestand) || Sluiten_Bestand(bestand) != -1 || foutnummer != 9) return 8;
    bestand = open_Bestand("tests.txt", alleen_lezen_WAARDE);
    if (bestand < 0 || schrijven_Bestand_gegevens(bestand, Inhoud_WAARDE, 1) != -1 || foutnummer != 9) return 9;
    if (Sluiten_Bestand(bestand)) return 10;
    bestand = open_Bestand("tests.txt", lezen_schrijven | 끝에이어쓰기);
    if (bestand < 0 || zoeken_Bestand(bestand, 0, 처음기준) != 0 || schrijven_Bestand_gegevens(bestand, "!", 1) != 1 || bestandsgrootte(bestand) != sizeof(Inhoud_WAARDE) + 1) return 11;
    if (set_Bestand_tijdsduur(bestand, 2) || zoeken_Bestand(bestand, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (schrijven_Bestand_gegevens(bestand, "x", 1) != 1 || bestandsgrootte(bestand) != 3 || Sluiten_Bestand(bestand)) return 13;
    bestand = open_Bestand("구멍.bin", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (bestand < 0 || zoeken_Bestand(bestand, 3, 처음기준) != 3 || schrijven_Bestand_gegevens(bestand, "z", 1) != 1) return 14;
    if (zoeken_Bestand(bestand, 0, 처음기준) != 0 || 파일자료읽기(bestand, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (verwijderen_Bestand_invoer_naam("구멍.bin") || bestandsgrootte(bestand) != 4 || Sluiten_Bestand(bestand)) return 16;
    if (open_Bestand("구멍.bin", alleen_lezen_WAARDE) != -1 || foutnummer != 2) return 17;
    if (open_Bestand("tests.txt", lezen_schrijven | 새파일만들기, 0600) != -1 || foutnummer != 17) return 18;
    if (open_Bestand("../금지", alleen_lezen_WAARDE) != -1) return 19;
    return 0;
}
