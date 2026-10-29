#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ maktaba 없는 freestanding C++11 programu_f5044b9b. 커널에 tuli_thamani 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char maudhui_thamani[] = "C++ → Java kiini_thamani_0611a8a8 · 한글 😀";
    unsigned char 읽은값[sizeof(maudhui_thamani)] = {};
    int faili = unda_faili("시험.txt", soma_andika | 없으면만들기 | 내용비우기, 0600);
    if (faili < 0) return 1;
    if (andika_faili_data(faili, maudhui_thamani, sizeof(maudhui_thamani)) != sizeof(maudhui_thamani)) return 2;
    if (tafuta_faili(faili, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(faili, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(maudhui_thamani); 순번++) if (읽은값[순번] != (unsigned char)maudhui_thamani[순번]) return 5;
    if (파일자료읽기(faili, 읽은값, 1) != 0) return 6;
    if (파일저장확정(faili) != -1 || 오류번호 != 38) return 7;
    if (funga_faili(faili) || funga_faili(faili) != -1 || 오류번호 != 9) return 8;
    faili = unda_faili("시험.txt", soma_tu_thamani);
    if (faili < 0 || andika_faili_data(faili, maudhui_thamani, 1) != -1 || 오류번호 != 9) return 9;
    if (funga_faili(faili)) return 10;
    faili = unda_faili("시험.txt", soma_andika | 끝에이어쓰기);
    if (faili < 0 || tafuta_faili(faili, 0, 처음기준) != 0 || andika_faili_data(faili, "!", 1) != 1 || faili_panga_ukubwa(faili) != sizeof(maudhui_thamani) + 1) return 11;
    if (seti_faili_urefu(faili, 2) || tafuta_faili(faili, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (andika_faili_data(faili, "x", 1) != 1 || faili_panga_ukubwa(faili) != 3 || funga_faili(faili)) return 13;
    faili = unda_faili("구멍.bin", soma_andika | 없으면만들기 | 내용비우기, 0600);
    if (faili < 0 || tafuta_faili(faili, 3, 처음기준) != 3 || andika_faili_data(faili, "z", 1) != 1) return 14;
    if (tafuta_faili(faili, 0, 처음기준) != 0 || 파일자료읽기(faili, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (ondoa_faili_ingizo_jina("구멍.bin") || faili_panga_ukubwa(faili) != 4 || funga_faili(faili)) return 16;
    if (unda_faili("구멍.bin", soma_tu_thamani) != -1 || 오류번호 != 2) return 17;
    if (unda_faili("시험.txt", soma_andika | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (unda_faili("../금지", soma_tu_thamani) != -1) return 19;
    return 0;
}
