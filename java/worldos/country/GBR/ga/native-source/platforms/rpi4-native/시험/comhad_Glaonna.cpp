#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ leabharlann 없는 freestanding C++11 clár_f5044b9b. 커널에 statach_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Inneachar_VALUE[] = "C++ → Java eithne_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Inneachar_VALUE)] = {};
    int Comhad = oscail_comhad("시험.txt", inléite_inscríofa | 없으면만들기 | 내용비우기, 0600);
    if (Comhad < 0) return 1;
    if (scríobh_comhad_sonraí(Comhad, Inneachar_VALUE, sizeof(Inneachar_VALUE)) != sizeof(Inneachar_VALUE)) return 2;
    if (lorg_comhad(Comhad, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Comhad, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Inneachar_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Inneachar_VALUE[순번]) return 5;
    if (파일자료읽기(Comhad, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Comhad) != -1 || 오류번호 != 38) return 7;
    if (dún_comhad(Comhad) || dún_comhad(Comhad) != -1 || 오류번호 != 9) return 8;
    Comhad = oscail_comhad("시험.txt", inléite_amháin_VALUE);
    if (Comhad < 0 || scríobh_comhad_sonraí(Comhad, Inneachar_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (dún_comhad(Comhad)) return 10;
    Comhad = oscail_comhad("시험.txt", inléite_inscríofa | 끝에이어쓰기);
    if (Comhad < 0 || lorg_comhad(Comhad, 0, 처음기준) != 0 || scríobh_comhad_sonraí(Comhad, "!", 1) != 1 || comhad_socraigh_méid(Comhad) != sizeof(Inneachar_VALUE) + 1) return 11;
    if (tacar_comhad_fad(Comhad, 2) || lorg_comhad(Comhad, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (scríobh_comhad_sonraí(Comhad, "x", 1) != 1 || comhad_socraigh_méid(Comhad) != 3 || dún_comhad(Comhad)) return 13;
    Comhad = oscail_comhad("구멍.bin", inléite_inscríofa | 없으면만들기 | 내용비우기, 0600);
    if (Comhad < 0 || lorg_comhad(Comhad, 3, 처음기준) != 3 || scríobh_comhad_sonraí(Comhad, "z", 1) != 1) return 14;
    if (lorg_comhad(Comhad, 0, 처음기준) != 0 || 파일자료읽기(Comhad, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (bain_comhad_iontráil_ainm("구멍.bin") || comhad_socraigh_méid(Comhad) != 4 || dún_comhad(Comhad)) return 16;
    if (oscail_comhad("구멍.bin", inléite_amháin_VALUE) != -1 || 오류번호 != 2) return 17;
    if (oscail_comhad("시험.txt", inléite_inscríofa | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (oscail_comhad("../금지", inléite_amháin_VALUE) != -1) return 19;
    return 0;
}
