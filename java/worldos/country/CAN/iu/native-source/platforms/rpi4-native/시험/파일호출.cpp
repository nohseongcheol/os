#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ tukisiurvik 없는 freestanding C++11 pilirijjut_f5044b9b. 커널에 surravviqanngittuq_atuutilik 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Ilulingit_atuutilik[] = "C++ → Java kernel_atuutilik · 한글 😀";
    unsigned char 읽은값[sizeof(Ilulingit_atuutilik)] = {};
    int ini = matuirli_ini("시험.txt", uqalimaarli_titirarli | 없으면만들기 | 내용비우기, 0600);
    if (ini < 0) return 1;
    if (titiraq_ini_titiqqat(ini, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik)) != sizeof(Ilulingit_atuutilik)) return 2;
    if (qinirli_ini(ini, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(ini, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Ilulingit_atuutilik); 순번++) if (읽은값[순번] != (unsigned char)Ilulingit_atuutilik[순번]) return 5;
    if (파일자료읽기(ini, 읽은값, 1) != 0) return 6;
    if (파일저장확정(ini) != -1 || 오류번호 != 38) return 7;
    if (matuli_ini(ini) || matuli_ini(ini) != -1 || 오류번호 != 9) return 8;
    ini = matuirli_ini("시험.txt", takugatuinnaq_atuutilik);
    if (ini < 0 || titiraq_ini_titiqqat(ini, Ilulingit_atuutilik, 1) != -1 || 오류번호 != 9) return 9;
    if (matuli_ini(ini)) return 10;
    ini = matuirli_ini("시험.txt", uqalimaarli_titirarli | 끝에이어쓰기);
    if (ini < 0 || qinirli_ini(ini, 0, 처음기준) != 0 || titiraq_ini_titiqqat(ini, "!", 1) != 1 || ini_anininga(ini) != sizeof(Ilulingit_atuutilik) + 1) return 11;
    if (attiqsimaniit_ini_takininga(ini, 2) || qinirli_ini(ini, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (titiraq_ini_titiqqat(ini, "x", 1) != 1 || ini_anininga(ini) != 3 || matuli_ini(ini)) return 13;
    ini = matuirli_ini("구멍.bin", uqalimaarli_titirarli | 없으면만들기 | 내용비우기, 0600);
    if (ini < 0 || qinirli_ini(ini, 3, 처음기준) != 3 || titiraq_ini_titiqqat(ini, "z", 1) != 1) return 14;
    if (qinirli_ini(ini, 0, 처음기준) != 0 || 파일자료읽기(ini, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (sanirvalli_ini_Iliniku_atiq("구멍.bin") || ini_anininga(ini) != 4 || matuli_ini(ini)) return 16;
    if (matuirli_ini("구멍.bin", takugatuinnaq_atuutilik) != -1 || 오류번호 != 2) return 17;
    if (matuirli_ini("시험.txt", uqalimaarli_titirarli | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (matuirli_ini("../금지", takugatuinnaq_atuutilik) != -1) return 19;
    return 0;
}
