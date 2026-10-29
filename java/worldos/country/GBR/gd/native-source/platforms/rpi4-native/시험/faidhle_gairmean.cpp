#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ leabhar_lann 없는 freestanding C++11 ap_f5044b9b. 커널에 stadaigeach_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char susbaint_VALUE[] = "C++ → Java eitean_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(susbaint_VALUE)] = {};
    int faidhle = fosgail_faidhle("시험.txt", so_leughte_so_sgrìobhte | 없으면만들기 | 내용비우기, 0600);
    if (faidhle < 0) return 1;
    if (sgrìobh_faidhle_dàta(faidhle, susbaint_VALUE, sizeof(susbaint_VALUE)) != sizeof(susbaint_VALUE)) return 2;
    if (sir_faidhle(faidhle, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(faidhle, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(susbaint_VALUE); 순번++) if (읽은값[순번] != (unsigned char)susbaint_VALUE[순번]) return 5;
    if (파일자료읽기(faidhle, 읽은값, 1) != 0) return 6;
    if (파일저장확정(faidhle) != -1 || 오류번호 != 38) return 7;
    if (dùin_faidhle(faidhle) || dùin_faidhle(faidhle) != -1 || 오류번호 != 9) return 8;
    faidhle = fosgail_faidhle("시험.txt", ri_leughadh_a_mhàin_VALUE);
    if (faidhle < 0 || sgrìobh_faidhle_dàta(faidhle, susbaint_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (dùin_faidhle(faidhle)) return 10;
    faidhle = fosgail_faidhle("시험.txt", so_leughte_so_sgrìobhte | 끝에이어쓰기);
    if (faidhle < 0 || sir_faidhle(faidhle, 0, 처음기준) != 0 || sgrìobh_faidhle_dàta(faidhle, "!", 1) != 1 || faidhle_atharraich_am_meud(faidhle) != sizeof(susbaint_VALUE) + 1) return 11;
    if (seata_faidhle_faid(faidhle, 2) || sir_faidhle(faidhle, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (sgrìobh_faidhle_dàta(faidhle, "x", 1) != 1 || faidhle_atharraich_am_meud(faidhle) != 3 || dùin_faidhle(faidhle)) return 13;
    faidhle = fosgail_faidhle("구멍.bin", so_leughte_so_sgrìobhte | 없으면만들기 | 내용비우기, 0600);
    if (faidhle < 0 || sir_faidhle(faidhle, 3, 처음기준) != 3 || sgrìobh_faidhle_dàta(faidhle, "z", 1) != 1) return 14;
    if (sir_faidhle(faidhle, 0, 처음기준) != 0 || 파일자료읽기(faidhle, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (thoir_air_falbh_faidhle_cur_a_steach_ainm("구멍.bin") || faidhle_atharraich_am_meud(faidhle) != 4 || dùin_faidhle(faidhle)) return 16;
    if (fosgail_faidhle("구멍.bin", ri_leughadh_a_mhàin_VALUE) != -1 || 오류번호 != 2) return 17;
    if (fosgail_faidhle("시험.txt", so_leughte_so_sgrìobhte | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (fosgail_faidhle("../금지", ri_leughadh_a_mhàin_VALUE) != -1) return 19;
    return 0;
}
