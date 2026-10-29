#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ laburare 없는 freestanding C++11 Shiri_f5044b9b. 커널에 Tsaye_cik_Daraja 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char kunshiya_Daraja[] = "C++ → Java Kwara_Daraja · 한글 😀";
    unsigned char 읽은값[sizeof(kunshiya_Daraja)] = {};
    int Fayil = buɗe_Fayil("시험.txt", Rubutuwa_karantuwa | 없으면만들기 | 내용비우기, 0600);
    if (Fayil < 0) return 1;
    if (Rubuta_Fayil_Tarin_bayani(Fayil, kunshiya_Daraja, sizeof(kunshiya_Daraja)) != sizeof(kunshiya_Daraja)) return 2;
    if (binciko_Fayil(Fayil, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fayil, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(kunshiya_Daraja); 순번++) if (읽은값[순번] != (unsigned char)kunshiya_Daraja[순번]) return 5;
    if (파일자료읽기(Fayil, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fayil) != -1 || 오류번호 != 38) return 7;
    if (Rufe_Fayil(Fayil) || Rufe_Fayil(Fayil) != -1 || 오류번호 != 9) return 8;
    Fayil = buɗe_Fayil("시험.txt", karanta_kawai_Daraja);
    if (Fayil < 0 || Rubuta_Fayil_Tarin_bayani(Fayil, kunshiya_Daraja, 1) != -1 || 오류번호 != 9) return 9;
    if (Rufe_Fayil(Fayil)) return 10;
    Fayil = buɗe_Fayil("시험.txt", Rubutuwa_karantuwa | 끝에이어쓰기);
    if (Fayil < 0 || binciko_Fayil(Fayil, 0, 처음기준) != 0 || Rubuta_Fayil_Tarin_bayani(Fayil, "!", 1) != 1 || Fayil_girma(Fayil) != sizeof(kunshiya_Daraja) + 1) return 11;
    if (zubi_Fayil_Tsawo(Fayil, 2) || binciko_Fayil(Fayil, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (Rubuta_Fayil_Tarin_bayani(Fayil, "x", 1) != 1 || Fayil_girma(Fayil) != 3 || Rufe_Fayil(Fayil)) return 13;
    Fayil = buɗe_Fayil("구멍.bin", Rubutuwa_karantuwa | 없으면만들기 | 내용비우기, 0600);
    if (Fayil < 0 || binciko_Fayil(Fayil, 3, 처음기준) != 3 || Rubuta_Fayil_Tarin_bayani(Fayil, "z", 1) != 1) return 14;
    if (binciko_Fayil(Fayil, 0, 처음기준) != 0 || 파일자료읽기(Fayil, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (Cire_Fayil_Mashigar_bayanai_Suna("구멍.bin") || Fayil_girma(Fayil) != 4 || Rufe_Fayil(Fayil)) return 16;
    if (buɗe_Fayil("구멍.bin", karanta_kawai_Daraja) != -1 || 오류번호 != 2) return 17;
    if (buɗe_Fayil("시험.txt", Rubutuwa_karantuwa | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (buɗe_Fayil("../금지", karanta_kawai_Daraja) != -1) return 19;
    return 0;
}
