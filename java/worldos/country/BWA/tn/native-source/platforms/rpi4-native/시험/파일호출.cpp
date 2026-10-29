#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ laeborari 없는 freestanding C++11 Tiriso_f5044b9b. 커널에 e_e_emeng_Boleng 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Diteng_Boleng[] = "C++ → Java Khenele_Boleng · 한글 😀";
    unsigned char 읽은값[sizeof(Diteng_Boleng)] = {};
    int faele = bula_faele("시험.txt", buisa_kwala | 없으면만들기 | 내용비우기, 0600);
    if (faele < 0) return 1;
    if (kwala_faele_tshedimosetso(faele, Diteng_Boleng, sizeof(Diteng_Boleng)) != sizeof(Diteng_Boleng)) return 2;
    if (batla_faele(faele, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(faele, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Diteng_Boleng); 순번++) if (읽은값[순번] != (unsigned char)Diteng_Boleng[순번]) return 5;
    if (파일자료읽기(faele, 읽은값, 1) != 0) return 6;
    if (파일저장확정(faele) != -1 || 오류번호 != 38) return 7;
    if (tswala_faele(faele) || tswala_faele(faele) != -1 || 오류번호 != 9) return 8;
    faele = bula_faele("시험.txt", puiso_fela_Boleng);
    if (faele < 0 || kwala_faele_tshedimosetso(faele, Diteng_Boleng, 1) != -1 || 오류번호 != 9) return 9;
    if (tswala_faele(faele)) return 10;
    faele = bula_faele("시험.txt", buisa_kwala | 끝에이어쓰기);
    if (faele < 0 || batla_faele(faele, 0, 처음기준) != 0 || kwala_faele_tshedimosetso(faele, "!", 1) != 1 || faele_lekanya(faele) != sizeof(Diteng_Boleng) + 1) return 11;
    if (sete_faele_boleele(faele, 2) || batla_faele(faele, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (kwala_faele_tshedimosetso(faele, "x", 1) != 1 || faele_lekanya(faele) != 3 || tswala_faele(faele)) return 13;
    faele = bula_faele("구멍.bin", buisa_kwala | 없으면만들기 | 내용비우기, 0600);
    if (faele < 0 || batla_faele(faele, 3, 처음기준) != 3 || kwala_faele_tshedimosetso(faele, "z", 1) != 1) return 14;
    if (batla_faele(faele, 0, 처음기준) != 0 || 파일자료읽기(faele, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (tlosa_faele_tsenyo_leina("구멍.bin") || faele_lekanya(faele) != 4 || tswala_faele(faele)) return 16;
    if (bula_faele("구멍.bin", puiso_fela_Boleng) != -1 || 오류번호 != 2) return 17;
    if (bula_faele("시험.txt", buisa_kwala | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (bula_faele("../금지", puiso_fela_Boleng) != -1) return 19;
    return 0;
}
