#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ daaray_téere 없는 freestanding C++11 jëfekaay_f5044b9b. 커널에 Soppeekoodi_xëyma 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Këmb_xëyma[] = "C++ → Java xoox_xëyma · 한글 😀";
    unsigned char 읽은값[sizeof(Këmb_xëyma)] = {};
    int bara_denc = sos_bara_denc("시험.txt", jàng_bind | 없으면만들기 | 내용비우기, 0600);
    if (bara_denc < 0) return 1;
    if (biir_bara_denc_mbir(bara_denc, Këmb_xëyma, sizeof(Këmb_xëyma)) != sizeof(Këmb_xëyma)) return 2;
    if (seet_bara_denc(bara_denc, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(bara_denc, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Këmb_xëyma); 순번++) if (읽은값[순번] != (unsigned char)Këmb_xëyma[순번]) return 5;
    if (파일자료읽기(bara_denc, 읽은값, 1) != 0) return 6;
    if (파일저장확정(bara_denc) != -1 || 오류번호 != 38) return 7;
    if (Tej_bara_denc(bara_denc) || Tej_bara_denc(bara_denc) != -1 || 오류번호 != 9) return 8;
    bara_denc = sos_bara_denc("시험.txt", ngir_jaŋarek_la_xëyma);
    if (bara_denc < 0 || biir_bara_denc_mbir(bara_denc, Këmb_xëyma, 1) != -1 || 오류번호 != 9) return 9;
    if (Tej_bara_denc(bara_denc)) return 10;
    bara_denc = sos_bara_denc("시험.txt", jàng_bind | 끝에이어쓰기);
    if (bara_denc < 0 || seet_bara_denc(bara_denc, 0, 처음기준) != 0 || biir_bara_denc_mbir(bara_denc, "!", 1) != 1 || bara_denc_tolluwaay(bara_denc) != sizeof(Këmb_xëyma) + 1) return 11;
    if (Boole_gi_bara_denc_diir(bara_denc, 2) || seet_bara_denc(bara_denc, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (biir_bara_denc_mbir(bara_denc, "x", 1) != 1 || bara_denc_tolluwaay(bara_denc) != 3 || Tej_bara_denc(bara_denc)) return 13;
    bara_denc = sos_bara_denc("구멍.bin", jàng_bind | 없으면만들기 | 내용비우기, 0600);
    if (bara_denc < 0 || seet_bara_denc(bara_denc, 3, 처음기준) != 3 || biir_bara_denc_mbir(bara_denc, "z", 1) != 1) return 14;
    if (seet_bara_denc(bara_denc, 0, 처음기준) != 0 || 파일자료읽기(bara_denc, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (dandal_bara_denc_dugal_xabaar_tur("구멍.bin") || bara_denc_tolluwaay(bara_denc) != 4 || Tej_bara_denc(bara_denc)) return 16;
    if (sos_bara_denc("구멍.bin", ngir_jaŋarek_la_xëyma) != -1 || 오류번호 != 2) return 17;
    if (sos_bara_denc("시험.txt", jàng_bind | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (sos_bara_denc("../금지", ngir_jaŋarek_la_xëyma) != -1) return 19;
    return 0;
}
