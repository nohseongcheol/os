#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ knjižnica 없는 freestanding C++11 aplikacija_f5044b9b. 커널에 statičen_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char vsebina_VALUE[] = "C++ → Java jedro_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(vsebina_VALUE)] = {};
    int Datoteka = odprto_Datoteka("시험.txt", branje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Datoteka < 0) return 1;
    if (pisati_Datoteka_podatki(Datoteka, vsebina_VALUE, sizeof(vsebina_VALUE)) != sizeof(vsebina_VALUE)) return 2;
    if (iskati_Datoteka(Datoteka, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Datoteka, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(vsebina_VALUE); 순번++) if (읽은값[순번] != (unsigned char)vsebina_VALUE[순번]) return 5;
    if (파일자료읽기(Datoteka, 읽은값, 1) != 0) return 6;
    if (potrjevanje_datotečna_shramba(Datoteka) != -1 || številka_napake != 38) return 7;
    if (Zapri_Datoteka(Datoteka) || Zapri_Datoteka(Datoteka) != -1 || številka_napake != 9) return 8;
    Datoteka = odprto_Datoteka("시험.txt", samo_za_branje_VALUE);
    if (Datoteka < 0 || pisati_Datoteka_podatki(Datoteka, vsebina_VALUE, 1) != -1 || številka_napake != 9) return 9;
    if (Zapri_Datoteka(Datoteka)) return 10;
    Datoteka = odprto_Datoteka("시험.txt", branje_pisanje | 끝에이어쓰기);
    if (Datoteka < 0 || iskati_Datoteka(Datoteka, 0, 처음기준) != 0 || pisati_Datoteka_podatki(Datoteka, "!", 1) != 1 || velikost_datoteke(Datoteka) != sizeof(vsebina_VALUE) + 1) return 11;
    if (파일길이정하기(Datoteka, 2) || iskati_Datoteka(Datoteka, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (pisati_Datoteka_podatki(Datoteka, "x", 1) != 1 || velikost_datoteke(Datoteka) != 3 || Zapri_Datoteka(Datoteka)) return 13;
    Datoteka = odprto_Datoteka("구멍.bin", branje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Datoteka < 0 || iskati_Datoteka(Datoteka, 3, 처음기준) != 3 || pisati_Datoteka_podatki(Datoteka, "z", 1) != 1) return 14;
    if (iskati_Datoteka(Datoteka, 0, 처음기준) != 0 || 파일자료읽기(Datoteka, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (odstraniti_Datoteka_vnos_ime("구멍.bin") || velikost_datoteke(Datoteka) != 4 || Zapri_Datoteka(Datoteka)) return 16;
    if (odprto_Datoteka("구멍.bin", samo_za_branje_VALUE) != -1 || številka_napake != 2) return 17;
    if (odprto_Datoteka("시험.txt", branje_pisanje | 새파일만들기, 0600) != -1 || številka_napake != 17) return 18;
    if (odprto_Datoteka("../금지", samo_za_branje_VALUE) != -1) return 19;
    return 0;
}
