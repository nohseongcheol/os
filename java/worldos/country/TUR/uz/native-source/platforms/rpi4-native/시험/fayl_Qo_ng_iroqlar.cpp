#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ kutubxona 없는 freestanding C++11 ilova_f5044b9b. 커널에 statik_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char tarkib_VALUE[] = "C++ → Java o_zak_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(tarkib_VALUE)] = {};
    int Fayl = ochmoq_fayl("시험.txt", o_qish_yozish_mumkin | 없으면만들기 | 내용비우기, 0600);
    if (Fayl < 0) return 1;
    if (yozmoq_fayl_ma_lumotlar(Fayl, tarkib_VALUE, sizeof(tarkib_VALUE)) != sizeof(tarkib_VALUE)) return 2;
    if (izlamoq_fayl(Fayl, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fayl, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(tarkib_VALUE); 순번++) if (읽은값[순번] != (unsigned char)tarkib_VALUE[순번]) return 5;
    if (파일자료읽기(Fayl, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fayl) != -1 || 오류번호 != 38) return 7;
    if (yopmoq_fayl(Fayl) || yopmoq_fayl(Fayl) != -1 || 오류번호 != 9) return 8;
    Fayl = ochmoq_fayl("시험.txt", faqat_o_qish_uchun_VALUE);
    if (Fayl < 0 || yozmoq_fayl_ma_lumotlar(Fayl, tarkib_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (yopmoq_fayl(Fayl)) return 10;
    Fayl = ochmoq_fayl("시험.txt", o_qish_yozish_mumkin | 끝에이어쓰기);
    if (Fayl < 0 || izlamoq_fayl(Fayl, 0, 처음기준) != 0 || yozmoq_fayl_ma_lumotlar(Fayl, "!", 1) != 1 || fayl_o_lcham(Fayl) != sizeof(tarkib_VALUE) + 1) return 11;
    if (to_plam_fayl_uzunlik(Fayl, 2) || izlamoq_fayl(Fayl, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (yozmoq_fayl_ma_lumotlar(Fayl, "x", 1) != 1 || fayl_o_lcham(Fayl) != 3 || yopmoq_fayl(Fayl)) return 13;
    Fayl = ochmoq_fayl("구멍.bin", o_qish_yozish_mumkin | 없으면만들기 | 내용비우기, 0600);
    if (Fayl < 0 || izlamoq_fayl(Fayl, 3, 처음기준) != 3 || yozmoq_fayl_ma_lumotlar(Fayl, "z", 1) != 1) return 14;
    if (izlamoq_fayl(Fayl, 0, 처음기준) != 0 || 파일자료읽기(Fayl, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (olib_tashlamoq_fayl_kiritish_nom("구멍.bin") || fayl_o_lcham(Fayl) != 4 || yopmoq_fayl(Fayl)) return 16;
    if (ochmoq_fayl("구멍.bin", faqat_o_qish_uchun_VALUE) != -1 || 오류번호 != 2) return 17;
    if (ochmoq_fayl("시험.txt", o_qish_yozish_mumkin | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (ochmoq_fayl("../금지", faqat_o_qish_uchun_VALUE) != -1) return 19;
    return 0;
}
