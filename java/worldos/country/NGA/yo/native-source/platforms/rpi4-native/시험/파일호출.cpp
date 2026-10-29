#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ ibi_ìpamọ́ 없는 freestanding C++11 àtòjọ_ètò_f5044b9b. 커널에 ìdágún_iye 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Àkóónú_iye[] = "C++ → Java kánẹ́ẹ̀lì_iye · 한글 😀";
    unsigned char 읽은값[sizeof(Àkóónú_iye)] = {};
    int Fáìlì = ṣí_fáìlì("시험.txt", tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600);
    if (Fáìlì < 0) return 1;
    if (kọ_fáìlì_détà(Fáìlì, Àkóónú_iye, sizeof(Àkóónú_iye)) != sizeof(Àkóónú_iye)) return 2;
    if (ṣàwárí_fáìlì(Fáìlì, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fáìlì, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Àkóónú_iye); 순번++) if (읽은값[순번] != (unsigned char)Àkóónú_iye[순번]) return 5;
    if (파일자료읽기(Fáìlì, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fáìlì) != -1 || 오류번호 != 38) return 7;
    if (pa_dé_fáìlì(Fáìlì) || pa_dé_fáìlì(Fáìlì) != -1 || 오류번호 != 9) return 8;
    Fáìlì = ṣí_fáìlì("시험.txt", kàn_kàá_iye);
    if (Fáìlì < 0 || kọ_fáìlì_détà(Fáìlì, Àkóónú_iye, 1) != -1 || 오류번호 != 9) return 9;
    if (pa_dé_fáìlì(Fáìlì)) return 10;
    Fáìlì = ṣí_fáìlì("시험.txt", tí_a_lè_kà_tí_a_lè_kọ | 끝에이어쓰기);
    if (Fáìlì < 0 || ṣàwárí_fáìlì(Fáìlì, 0, 처음기준) != 0 || kọ_fáìlì_détà(Fáìlì, "!", 1) != 1 || fáìlì_ìwọn(Fáìlì) != sizeof(Àkóónú_iye) + 1) return 11;
    if (ọ̀wọ̀_fáìlì_gígùn(Fáìlì, 2) || ṣàwárí_fáìlì(Fáìlì, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (kọ_fáìlì_détà(Fáìlì, "x", 1) != 1 || fáìlì_ìwọn(Fáìlì) != 3 || pa_dé_fáìlì(Fáìlì)) return 13;
    Fáìlì = ṣí_fáìlì("구멍.bin", tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600);
    if (Fáìlì < 0 || ṣàwárí_fáìlì(Fáìlì, 3, 처음기준) != 3 || kọ_fáìlì_détà(Fáìlì, "z", 1) != 1) return 14;
    if (ṣàwárí_fáìlì(Fáìlì, 0, 처음기준) != 0 || 파일자료읽기(Fáìlì, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ("구멍.bin") || fáìlì_ìwọn(Fáìlì) != 4 || pa_dé_fáìlì(Fáìlì)) return 16;
    if (ṣí_fáìlì("구멍.bin", kàn_kàá_iye) != -1 || 오류번호 != 2) return 17;
    if (ṣí_fáìlì("시험.txt", tí_a_lè_kà_tí_a_lè_kọ | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (ṣí_fáìlì("../금지", kàn_kàá_iye) != -1) return 19;
    return 0;
}
