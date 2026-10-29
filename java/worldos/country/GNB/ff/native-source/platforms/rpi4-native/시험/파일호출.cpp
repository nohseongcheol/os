#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ defterdu 없는 freestanding C++11 tafirde_f5044b9b. 커널에 ñiiɓ_njaru 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char loowdi_njaru[] = "C++ → Java aaluude_njaru · 한글 😀";
    unsigned char 읽은값[sizeof(loowdi_njaru)] = {};
    int fiilde = udditde_fiilde("시험.txt", tar_winndu | 없으면만들기 | 내용비우기, 0600);
    if (fiilde < 0) return 1;
    if (winndude_fiilde_keɓe(fiilde, loowdi_njaru, sizeof(loowdi_njaru)) != sizeof(loowdi_njaru)) return 2;
    if (파일위치옮기기(fiilde, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(fiilde, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(loowdi_njaru); 순번++) if (읽은값[순번] != (unsigned char)loowdi_njaru[순번]) return 5;
    if (파일자료읽기(fiilde, 읽은값, 1) != 0) return 6;
    if (파일저장확정(fiilde) != -1 || 오류번호 != 38) return 7;
    if (uddude_fiilde(fiilde) || uddude_fiilde(fiilde) != -1 || 오류번호 != 9) return 8;
    fiilde = udditde_fiilde("시험.txt", janngotooɗo_tan_njaru);
    if (fiilde < 0 || winndude_fiilde_keɓe(fiilde, loowdi_njaru, 1) != -1 || 오류번호 != 9) return 9;
    if (uddude_fiilde(fiilde)) return 10;
    fiilde = udditde_fiilde("시험.txt", tar_winndu | 끝에이어쓰기);
    if (fiilde < 0 || 파일위치옮기기(fiilde, 0, 처음기준) != 0 || winndude_fiilde_keɓe(fiilde, "!", 1) != 1 || fiilde_waylude_etannde(fiilde) != sizeof(loowdi_njaru) + 1) return 11;
    if (파일길이정하기(fiilde, 2) || 파일위치옮기기(fiilde, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (winndude_fiilde_keɓe(fiilde, "x", 1) != 1 || fiilde_waylude_etannde(fiilde) != 3 || uddude_fiilde(fiilde)) return 13;
    fiilde = udditde_fiilde("구멍.bin", tar_winndu | 없으면만들기 | 내용비우기, 0600);
    if (fiilde < 0 || 파일위치옮기기(fiilde, 3, 처음기준) != 3 || winndude_fiilde_keɓe(fiilde, "z", 1) != 1) return 14;
    if (파일위치옮기기(fiilde, 0, 처음기준) != 0 || 파일자료읽기(fiilde, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (ittude_fiilde_naatnugol_innde("구멍.bin") || fiilde_waylude_etannde(fiilde) != 4 || uddude_fiilde(fiilde)) return 16;
    if (udditde_fiilde("구멍.bin", janngotooɗo_tan_njaru) != -1 || 오류번호 != 2) return 17;
    if (udditde_fiilde("시험.txt", tar_winndu | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (udditde_fiilde("../금지", janngotooɗo_tan_njaru) != -1) return 19;
    return 0;
}
