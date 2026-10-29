#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ umtapo 없는 freestanding C++11 i_app_f5044b9b. 커널에 ngaguquki_inani 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Okuqukethwe_inani[] = "C++ → Java ikhenela_inani · 한글 😀";
    unsigned char 읽은값[sizeof(Okuqukethwe_inani)] = {};
    int Ihele = vula_ifayela("시험.txt", fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600);
    if (Ihele < 0) return 1;
    if (bhala_ifayela_imininingwane(Ihele, Okuqukethwe_inani, sizeof(Okuqukethwe_inani)) != sizeof(Okuqukethwe_inani)) return 2;
    if (cinga_ifayela(Ihele, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Ihele, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Okuqukethwe_inani); 순번++) if (읽은값[순번] != (unsigned char)Okuqukethwe_inani[순번]) return 5;
    if (파일자료읽기(Ihele, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Ihele) != -1 || 오류번호 != 38) return 7;
    if (vala_ifayela(Ihele) || vala_ifayela(Ihele) != -1 || 오류번호 != 9) return 8;
    Ihele = vula_ifayela("시험.txt", fundwayo_kuphela_inani);
    if (Ihele < 0 || bhala_ifayela_imininingwane(Ihele, Okuqukethwe_inani, 1) != -1 || 오류번호 != 9) return 9;
    if (vala_ifayela(Ihele)) return 10;
    Ihele = vula_ifayela("시험.txt", fundeka_bhaleka | 끝에이어쓰기);
    if (Ihele < 0 || cinga_ifayela(Ihele, 0, 처음기준) != 0 || bhala_ifayela_imininingwane(Ihele, "!", 1) != 1 || ifayela_linganisa(Ihele) != sizeof(Okuqukethwe_inani) + 1) return 11;
    if (isethi_ifayela_ubude(Ihele, 2) || cinga_ifayela(Ihele, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (bhala_ifayela_imininingwane(Ihele, "x", 1) != 1 || ifayela_linganisa(Ihele) != 3 || vala_ifayela(Ihele)) return 13;
    Ihele = vula_ifayela("구멍.bin", fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600);
    if (Ihele < 0 || cinga_ifayela(Ihele, 3, 처음기준) != 3 || bhala_ifayela_imininingwane(Ihele, "z", 1) != 1) return 14;
    if (cinga_ifayela(Ihele, 0, 처음기준) != 0 || 파일자료읽기(Ihele, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (khipha_ifayela_okufakwayo_igama("구멍.bin") || ifayela_linganisa(Ihele) != 4 || vala_ifayela(Ihele)) return 16;
    if (vula_ifayela("구멍.bin", fundwayo_kuphela_inani) != -1 || 오류번호 != 2) return 17;
    if (vula_ifayela("시험.txt", fundeka_bhaleka | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (vula_ifayela("../금지", fundwayo_kuphela_inani) != -1) return 19;
    return 0;
}
