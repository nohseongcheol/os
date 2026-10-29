#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ biblioteek 없는 freestanding C++11 program_f5044b9b. 커널에 staties_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Inhoud_VALUE[] = "C++ → Java kern_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Inhoud_VALUE)] = {};
    int Lêer = skep_lêer("시험.txt", lees_skryf | 없으면만들기 | 내용비우기, 0600);
    if (Lêer < 0) return 1;
    if (skryf_lêer_data(Lêer, Inhoud_VALUE, sizeof(Inhoud_VALUE)) != sizeof(Inhoud_VALUE)) return 2;
    if (soek_lêer(Lêer, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Lêer, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Inhoud_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Inhoud_VALUE[순번]) return 5;
    if (파일자료읽기(Lêer, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Lêer) != -1 || 오류번호 != 38) return 7;
    if (sluit_lêer(Lêer) || sluit_lêer(Lêer) != -1 || 오류번호 != 9) return 8;
    Lêer = skep_lêer("시험.txt", leesalleen_VALUE);
    if (Lêer < 0 || skryf_lêer_data(Lêer, Inhoud_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (sluit_lêer(Lêer)) return 10;
    Lêer = skep_lêer("시험.txt", lees_skryf | 끝에이어쓰기);
    if (Lêer < 0 || soek_lêer(Lêer, 0, 처음기준) != 0 || skryf_lêer_data(Lêer, "!", 1) != 1 || lêer_verstel(Lêer) != sizeof(Inhoud_VALUE) + 1) return 11;
    if (stel_lêer_lengte(Lêer, 2) || soek_lêer(Lêer, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (skryf_lêer_data(Lêer, "x", 1) != 1 || lêer_verstel(Lêer) != 3 || sluit_lêer(Lêer)) return 13;
    Lêer = skep_lêer("구멍.bin", lees_skryf | 없으면만들기 | 내용비우기, 0600);
    if (Lêer < 0 || soek_lêer(Lêer, 3, 처음기준) != 3 || skryf_lêer_data(Lêer, "z", 1) != 1) return 14;
    if (soek_lêer(Lêer, 0, 처음기준) != 0 || 파일자료읽기(Lêer, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (verwyder_lêer_inskrywing_naam("구멍.bin") || lêer_verstel(Lêer) != 4 || sluit_lêer(Lêer)) return 16;
    if (skep_lêer("구멍.bin", leesalleen_VALUE) != -1 || 오류번호 != 2) return 17;
    if (skep_lêer("시험.txt", lees_skryf | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (skep_lêer("../금지", leesalleen_VALUE) != -1) return 19;
    return 0;
}
