#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ ilayibhrari 없는 freestanding C++11 inkqubo_f5044b9b. 커널에 imi_ndawonye_ixabiso 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Isiqulatho_ixabiso[] = "C++ → Java ikheneli_ixabiso · 한글 😀";
    unsigned char 읽은값[sizeof(Isiqulatho_ixabiso)] = {};
    int iFayili = vula_ifayile("시험.txt", funda_bhala | 없으면만들기 | 내용비우기, 0600);
    if (iFayili < 0) return 1;
    if (bhala_ifayile_iingcombolo(iFayili, Isiqulatho_ixabiso, sizeof(Isiqulatho_ixabiso)) != sizeof(Isiqulatho_ixabiso)) return 2;
    if (khangela_ifayile(iFayili, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(iFayili, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Isiqulatho_ixabiso); 순번++) if (읽은값[순번] != (unsigned char)Isiqulatho_ixabiso[순번]) return 5;
    if (파일자료읽기(iFayili, 읽은값, 1) != 0) return 6;
    if (파일저장확정(iFayili) != -1 || 오류번호 != 38) return 7;
    if (vala_ifayile(iFayili) || vala_ifayile(iFayili) != -1 || 오류번호 != 9) return 8;
    iFayili = vula_ifayile("시험.txt", efundwayo_kuphela_ixabiso);
    if (iFayili < 0 || bhala_ifayile_iingcombolo(iFayili, Isiqulatho_ixabiso, 1) != -1 || 오류번호 != 9) return 9;
    if (vala_ifayile(iFayili)) return 10;
    iFayili = vula_ifayile("시험.txt", funda_bhala | 끝에이어쓰기);
    if (iFayili < 0 || khangela_ifayile(iFayili, 0, 처음기준) != 0 || bhala_ifayile_iingcombolo(iFayili, "!", 1) != 1 || ifayile_isayizi(iFayili) != sizeof(Isiqulatho_ixabiso) + 1) return 11;
    if (isethi_ifayile_ubude(iFayili, 2) || khangela_ifayile(iFayili, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (bhala_ifayile_iingcombolo(iFayili, "x", 1) != 1 || ifayile_isayizi(iFayili) != 3 || vala_ifayile(iFayili)) return 13;
    iFayili = vula_ifayile("구멍.bin", funda_bhala | 없으면만들기 | 내용비우기, 0600);
    if (iFayili < 0 || khangela_ifayile(iFayili, 3, 처음기준) != 3 || bhala_ifayile_iingcombolo(iFayili, "z", 1) != 1) return 14;
    if (khangela_ifayile(iFayili, 0, 처음기준) != 0 || 파일자료읽기(iFayili, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (shenxisa_ifayile_ufako_nkcukacha_igama("구멍.bin") || ifayile_isayizi(iFayili) != 4 || vala_ifayile(iFayili)) return 16;
    if (vula_ifayile("구멍.bin", efundwayo_kuphela_ixabiso) != -1 || 오류번호 != 2) return 17;
    if (vula_ifayile("시험.txt", funda_bhala | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (vula_ifayile("../금지", efundwayo_kuphela_ixabiso) != -1) return 19;
    return 0;
}
