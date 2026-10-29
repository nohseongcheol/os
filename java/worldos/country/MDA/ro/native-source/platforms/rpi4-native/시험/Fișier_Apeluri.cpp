#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotecă 없는 freestanding C++11 program_f5044b9b. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Conținut_VALUE[] = "C++ → Java nucleu_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Conținut_VALUE)] = {};
    int Fișier = crea_Fișier("시험.txt", citire_scriere | 없으면만들기 | trunchia_TOC, 0600);
    if (Fișier < 0) return 1;
    if (scriere_Fișier_date(Fișier, Conținut_VALUE, sizeof(Conținut_VALUE)) != sizeof(Conținut_VALUE)) return 2;
    if (căuta_Fișier(Fișier, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fișier, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Conținut_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Conținut_VALUE[순번]) return 5;
    if (파일자료읽기(Fișier, 읽은값, 1) != 0) return 6;
    if (comitere_Fișiere(Fișier) != -1 || număr_de_eroare != 38) return 7;
    if (închide_Fișier(Fișier) || închide_Fișier(Fișier) != -1 || număr_de_eroare != 9) return 8;
    Fișier = crea_Fișier("시험.txt", doar_în_citire_VALUE);
    if (Fișier < 0 || scriere_Fișier_date(Fișier, Conținut_VALUE, 1) != -1 || număr_de_eroare != 9) return 9;
    if (închide_Fișier(Fișier)) return 10;
    Fișier = crea_Fișier("시험.txt", citire_scriere | 끝에이어쓰기);
    if (Fișier < 0 || căuta_Fișier(Fișier, 0, 처음기준) != 0 || scriere_Fișier_date(Fișier, "!", 1) != 1 || dimensiune_fișier(Fișier) != sizeof(Conținut_VALUE) + 1) return 11;
    if (set_Fișier_lungime(Fișier, 2) || căuta_Fișier(Fișier, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (scriere_Fișier_date(Fișier, "x", 1) != 1 || dimensiune_fișier(Fișier) != 3 || închide_Fișier(Fișier)) return 13;
    Fișier = crea_Fișier("구멍.bin", citire_scriere | 없으면만들기 | trunchia_TOC, 0600);
    if (Fișier < 0 || căuta_Fișier(Fișier, 3, 처음기준) != 3 || scriere_Fișier_date(Fișier, "z", 1) != 1) return 14;
    if (căuta_Fișier(Fișier, 0, 처음기준) != 0 || 파일자료읽기(Fișier, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (elimina_Fișier_intrare_nume("구멍.bin") || dimensiune_fișier(Fișier) != 4 || închide_Fișier(Fișier)) return 16;
    if (crea_Fișier("구멍.bin", doar_în_citire_VALUE) != -1 || număr_de_eroare != 2) return 17;
    if (crea_Fișier("시험.txt", citire_scriere | 새파일만들기, 0600) != -1 || număr_de_eroare != 17) return 18;
    if (crea_Fișier("../금지", doar_în_citire_VALUE) != -1) return 19;
    return 0;
}
