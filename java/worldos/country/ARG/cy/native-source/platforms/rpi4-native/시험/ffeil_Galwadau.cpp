#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ llyfrgell 없는 freestanding C++11 Rhaglen_f5044b9b. 커널에 statig_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Cynnwys_VALUE[] = "C++ → Java cnewyllyn_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Cynnwys_VALUE)] = {};
    int Ffeil = agor_ffeil("시험.txt", darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600);
    if (Ffeil < 0) return 1;
    if (ysgrifennu_ffeil_data(Ffeil, Cynnwys_VALUE, sizeof(Cynnwys_VALUE)) != sizeof(Cynnwys_VALUE)) return 2;
    if (chwilio_ffeil(Ffeil, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Ffeil, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Cynnwys_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Cynnwys_VALUE[순번]) return 5;
    if (파일자료읽기(Ffeil, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Ffeil) != -1 || 오류번호 != 38) return 7;
    if (cau_ffeil(Ffeil) || cau_ffeil(Ffeil) != -1 || 오류번호 != 9) return 8;
    Ffeil = agor_ffeil("시험.txt", darllen_yn_unig_VALUE);
    if (Ffeil < 0 || ysgrifennu_ffeil_data(Ffeil, Cynnwys_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (cau_ffeil(Ffeil)) return 10;
    Ffeil = agor_ffeil("시험.txt", darllen_ysgrifennu | 끝에이어쓰기);
    if (Ffeil < 0 || chwilio_ffeil(Ffeil, 0, 처음기준) != 0 || ysgrifennu_ffeil_data(Ffeil, "!", 1) != 1 || ffeil_newid_maint(Ffeil) != sizeof(Cynnwys_VALUE) + 1) return 11;
    if (set_ffeil_hyd(Ffeil, 2) || chwilio_ffeil(Ffeil, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (ysgrifennu_ffeil_data(Ffeil, "x", 1) != 1 || ffeil_newid_maint(Ffeil) != 3 || cau_ffeil(Ffeil)) return 13;
    Ffeil = agor_ffeil("구멍.bin", darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600);
    if (Ffeil < 0 || chwilio_ffeil(Ffeil, 3, 처음기준) != 3 || ysgrifennu_ffeil_data(Ffeil, "z", 1) != 1) return 14;
    if (chwilio_ffeil(Ffeil, 0, 처음기준) != 0 || 파일자료읽기(Ffeil, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (tynnu_ffeil_cofnod_enw("구멍.bin") || ffeil_newid_maint(Ffeil) != 4 || cau_ffeil(Ffeil)) return 16;
    if (agor_ffeil("구멍.bin", darllen_yn_unig_VALUE) != -1 || 오류번호 != 2) return 17;
    if (agor_ffeil("시험.txt", darllen_ysgrifennu | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (agor_ffeil("../금지", darllen_yn_unig_VALUE) != -1) return 19;
    return 0;
}
