#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ librerija 없는 freestanding C++11 programm_f5044b9b. 커널에 statiku_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Kontenut_VALUE[] = "C++ → Java kernel_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Kontenut_VALUE)] = {};
    int fajl = fetaħ_fajl("시험.txt", qari_kitba | 없으면만들기 | 내용비우기, 0600);
    if (fajl < 0) return 1;
    if (kiteb_fajl_data(fajl, Kontenut_VALUE, sizeof(Kontenut_VALUE)) != sizeof(Kontenut_VALUE)) return 2;
    if (fittex_fajl(fajl, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(fajl, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Kontenut_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Kontenut_VALUE[순번]) return 5;
    if (파일자료읽기(fajl, 읽은값, 1) != 0) return 6;
    if (파일저장확정(fajl) != -1 || 오류번호 != 38) return 7;
    if (agħlaq_fajl(fajl) || agħlaq_fajl(fajl) != -1 || 오류번호 != 9) return 8;
    fajl = fetaħ_fajl("시험.txt", qari_biss_VALUE);
    if (fajl < 0 || kiteb_fajl_data(fajl, Kontenut_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (agħlaq_fajl(fajl)) return 10;
    fajl = fetaħ_fajl("시험.txt", qari_kitba | 끝에이어쓰기);
    if (fajl < 0 || fittex_fajl(fajl, 0, 처음기준) != 0 || kiteb_fajl_data(fajl, "!", 1) != 1 || fajl_daqqas(fajl) != sizeof(Kontenut_VALUE) + 1) return 11;
    if (sett_fajl_tul(fajl, 2) || fittex_fajl(fajl, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (kiteb_fajl_data(fajl, "x", 1) != 1 || fajl_daqqas(fajl) != 3 || agħlaq_fajl(fajl)) return 13;
    fajl = fetaħ_fajl("구멍.bin", qari_kitba | 없으면만들기 | 내용비우기, 0600);
    if (fajl < 0 || fittex_fajl(fajl, 3, 처음기준) != 3 || kiteb_fajl_data(fajl, "z", 1) != 1) return 14;
    if (fittex_fajl(fajl, 0, 처음기준) != 0 || 파일자료읽기(fajl, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (neħħa_fajl_entrata_isem("구멍.bin") || fajl_daqqas(fajl) != 4 || agħlaq_fajl(fajl)) return 16;
    if (fetaħ_fajl("구멍.bin", qari_biss_VALUE) != -1 || 오류번호 != 2) return 17;
    if (fetaħ_fajl("시험.txt", qari_kitba | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (fetaħ_fajl("../금지", qari_biss_VALUE) != -1) return 19;
    return 0;
}
