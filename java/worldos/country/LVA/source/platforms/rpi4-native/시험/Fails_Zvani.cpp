#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ bibliotēka 없는 freestanding C++11 programma_f5044b9b. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Saturs_VALUE[] = "C++ → Java kodols_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Saturs_VALUE)] = {};
    int Fails = atvērt_Fails("시험.txt", 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600);
    if (Fails < 0) return 1;
    if (rakstīšana_Fails_dati(Fails, Saturs_VALUE, sizeof(Saturs_VALUE)) != sizeof(Saturs_VALUE)) return 2;
    if (meklēt_Fails(Fails, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fails, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Saturs_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Saturs_VALUE[순번]) return 5;
    if (파일자료읽기(Fails, 읽은값, 1) != 0) return 6;
    if (izpilde_failu_krātuve(Fails) != -1 || kļūdas_numurs != 38) return 7;
    if (Aizvērt_Fails(Fails) || Aizvērt_Fails(Fails) != -1 || kļūdas_numurs != 9) return 8;
    Fails = atvērt_Fails("시험.txt", tikai_lasāms_VALUE);
    if (Fails < 0 || rakstīšana_Fails_dati(Fails, Saturs_VALUE, 1) != -1 || kļūdas_numurs != 9) return 9;
    if (Aizvērt_Fails(Fails)) return 10;
    Fails = atvērt_Fails("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (Fails < 0 || meklēt_Fails(Fails, 0, 처음기준) != 0 || rakstīšana_Fails_dati(Fails, "!", 1) != 1 || faila_lielums(Fails) != sizeof(Saturs_VALUE) + 1) return 11;
    if (파일길이정하기(Fails, 2) || meklēt_Fails(Fails, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (rakstīšana_Fails_dati(Fails, "x", 1) != 1 || faila_lielums(Fails) != 3 || Aizvērt_Fails(Fails)) return 13;
    Fails = atvērt_Fails("구멍.bin", 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600);
    if (Fails < 0 || meklēt_Fails(Fails, 3, 처음기준) != 3 || rakstīšana_Fails_dati(Fails, "z", 1) != 1) return 14;
    if (meklēt_Fails(Fails, 0, 처음기준) != 0 || 파일자료읽기(Fails, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (noņemt_Fails_ievade_nosaukums("구멍.bin") || faila_lielums(Fails) != 4 || Aizvērt_Fails(Fails)) return 16;
    if (atvērt_Fails("구멍.bin", tikai_lasāms_VALUE) != -1 || kļūdas_numurs != 2) return 17;
    if (atvērt_Fails("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || kļūdas_numurs != 17) return 18;
    if (atvērt_Fails("../금지", tikai_lasāms_VALUE) != -1) return 19;
    return 0;
}
