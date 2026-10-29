#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ Bokgobadata 없는 freestanding C++11 tirišo_f5044b9b. 커널에 ya_go_se_fetoge_boleng_f430d3f5 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Diteng_boleng[] = "C++ → Java khenele_boleng · 한글 😀";
    unsigned char 읽은값[sizeof(Diteng_boleng)] = {};
    int Faele = bula_faele("시험.txt", bala_ngwala | 없으면만들기 | 내용비우기, 0600);
    if (Faele < 0) return 1;
    if (ngwala_faele_data(Faele, Diteng_boleng, sizeof(Diteng_boleng)) != sizeof(Diteng_boleng)) return 2;
    if (nyaka_faele(Faele, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Faele, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Diteng_boleng); 순번++) if (읽은값[순번] != (unsigned char)Diteng_boleng[순번]) return 5;
    if (파일자료읽기(Faele, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Faele) != -1 || 오류번호 != 38) return 7;
    if (tswalela_faele(Faele) || tswalela_faele(Faele) != -1 || 오류번호 != 9) return 8;
    Faele = bula_faele("시험.txt", balwago_fela_boleng);
    if (Faele < 0 || ngwala_faele_data(Faele, Diteng_boleng, 1) != -1 || 오류번호 != 9) return 9;
    if (tswalela_faele(Faele)) return 10;
    Faele = bula_faele("시험.txt", bala_ngwala | 끝에이어쓰기);
    if (Faele < 0 || nyaka_faele(Faele, 0, 처음기준) != 0 || ngwala_faele_data(Faele, "!", 1) != 1 || faele_bogolo(Faele) != sizeof(Diteng_boleng) + 1) return 11;
    if (sehlopha_faele_botelele(Faele, 2) || nyaka_faele(Faele, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (ngwala_faele_data(Faele, "x", 1) != 1 || faele_bogolo(Faele) != 3 || tswalela_faele(Faele)) return 13;
    Faele = bula_faele("구멍.bin", bala_ngwala | 없으면만들기 | 내용비우기, 0600);
    if (Faele < 0 || nyaka_faele(Faele, 3, 처음기준) != 3 || ngwala_faele_data(Faele, "z", 1) != 1) return 14;
    if (nyaka_faele(Faele, 0, 처음기준) != 0 || 파일자료읽기(Faele, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (tloša_faele_go_tsenya_tshedimošo_leina("구멍.bin") || faele_bogolo(Faele) != 4 || tswalela_faele(Faele)) return 16;
    if (bula_faele("구멍.bin", balwago_fela_boleng) != -1 || 오류번호 != 2) return 17;
    if (bula_faele("시험.txt", bala_ngwala | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (bula_faele("../금지", balwago_fela_boleng) != -1) return 19;
    return 0;
}
