#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ biblioteka 없는 freestanding C++11 program_f5044b9b. 커널에 statični_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Sadržaj_VALUE[] = "C++ → Java jezgro_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Sadržaj_VALUE)] = {};
    int Fajl = kreirati_fajl("시험.txt", i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Fajl < 0) return 1;
    if (pisati_fajl_podaci(Fajl, Sadržaj_VALUE, sizeof(Sadržaj_VALUE)) != sizeof(Sadržaj_VALUE)) return 2;
    if (tražiti_fajl(Fajl, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fajl, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Sadržaj_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Sadržaj_VALUE[순번]) return 5;
    if (파일자료읽기(Fajl, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fajl) != -1 || broj_greške != 38) return 7;
    if (zatvoriti_fajl(Fajl) || zatvoriti_fajl(Fajl) != -1 || broj_greške != 9) return 8;
    Fajl = kreirati_fajl("시험.txt", samo_za_čitanje_VALUE);
    if (Fajl < 0 || pisati_fajl_podaci(Fajl, Sadržaj_VALUE, 1) != -1 || broj_greške != 9) return 9;
    if (zatvoriti_fajl(Fajl)) return 10;
    Fajl = kreirati_fajl("시험.txt", i_za_čitanje_i_za_pisanje | 끝에이어쓰기);
    if (Fajl < 0 || tražiti_fajl(Fajl, 0, 처음기준) != 0 || pisati_fajl_podaci(Fajl, "!", 1) != 1 || fajl_podesiti_veličinu(Fajl) != sizeof(Sadržaj_VALUE) + 1) return 11;
    if (skup_fajl_dužina(Fajl, 2) || tražiti_fajl(Fajl, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (pisati_fajl_podaci(Fajl, "x", 1) != 1 || fajl_podesiti_veličinu(Fajl) != 3 || zatvoriti_fajl(Fajl)) return 13;
    Fajl = kreirati_fajl("구멍.bin", i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Fajl < 0 || tražiti_fajl(Fajl, 3, 처음기준) != 3 || pisati_fajl_podaci(Fajl, "z", 1) != 1) return 14;
    if (tražiti_fajl(Fajl, 0, 처음기준) != 0 || 파일자료읽기(Fajl, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (ukloniti_fajl_unos_naziv("구멍.bin") || fajl_podesiti_veličinu(Fajl) != 4 || zatvoriti_fajl(Fajl)) return 16;
    if (kreirati_fajl("구멍.bin", samo_za_čitanje_VALUE) != -1 || broj_greške != 2) return 17;
    if (kreirati_fajl("시험.txt", i_za_čitanje_i_za_pisanje | 새파일만들기, 0600) != -1 || broj_greške != 17) return 18;
    if (kreirati_fajl("../금지", samo_za_čitanje_VALUE) != -1) return 19;
    return 0;
}
