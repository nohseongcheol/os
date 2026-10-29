#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ biblioteka 없는 freestanding C++11 program_f5044b9b. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Sadržaj_VALUE[] = "C++ → Java jezgra_sustava_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Sadržaj_VALUE)] = {};
    int Datoteka = otvoreno_Datoteka("시험.txt", 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600);
    if (Datoteka < 0) return 1;
    if (zapisivanje_Datoteka_podaci(Datoteka, Sadržaj_VALUE, sizeof(Sadržaj_VALUE)) != sizeof(Sadržaj_VALUE)) return 2;
    if (tražiti_Datoteka(Datoteka, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Datoteka, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Sadržaj_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Sadržaj_VALUE[순번]) return 5;
    if (파일자료읽기(Datoteka, 읽은값, 1) != 0) return 6;
    if (izvršavanje_pohrana_datoteka(Datoteka) != -1 || broj_pogreške != 38) return 7;
    if (Zatvori_Datoteka(Datoteka) || Zatvori_Datoteka(Datoteka) != -1 || broj_pogreške != 9) return 8;
    Datoteka = otvoreno_Datoteka("시험.txt", samo_za_čitanje_VALUE);
    if (Datoteka < 0 || zapisivanje_Datoteka_podaci(Datoteka, Sadržaj_VALUE, 1) != -1 || broj_pogreške != 9) return 9;
    if (Zatvori_Datoteka(Datoteka)) return 10;
    Datoteka = otvoreno_Datoteka("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (Datoteka < 0 || tražiti_Datoteka(Datoteka, 0, 처음기준) != 0 || zapisivanje_Datoteka_podaci(Datoteka, "!", 1) != 1 || veličina_datoteke(Datoteka) != sizeof(Sadržaj_VALUE) + 1) return 11;
    if (파일길이정하기(Datoteka, 2) || tražiti_Datoteka(Datoteka, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (zapisivanje_Datoteka_podaci(Datoteka, "x", 1) != 1 || veličina_datoteke(Datoteka) != 3 || Zatvori_Datoteka(Datoteka)) return 13;
    Datoteka = otvoreno_Datoteka("구멍.bin", 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600);
    if (Datoteka < 0 || tražiti_Datoteka(Datoteka, 3, 처음기준) != 3 || zapisivanje_Datoteka_podaci(Datoteka, "z", 1) != 1) return 14;
    if (tražiti_Datoteka(Datoteka, 0, 처음기준) != 0 || 파일자료읽기(Datoteka, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (ukloniti_Datoteka_unos_naziv("구멍.bin") || veličina_datoteke(Datoteka) != 4 || Zatvori_Datoteka(Datoteka)) return 16;
    if (otvoreno_Datoteka("구멍.bin", samo_za_čitanje_VALUE) != -1 || broj_pogreške != 2) return 17;
    if (otvoreno_Datoteka("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || broj_pogreške != 17) return 18;
    if (otvoreno_Datoteka("../금지", samo_za_čitanje_VALUE) != -1) return 19;
    return 0;
}
