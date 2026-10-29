#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ kitabxana 없는 freestanding C++11 proqram_f5044b9b. 커널에 statik_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Məzmun_VALUE[] = "C++ → Java nüvə_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Məzmun_VALUE)] = {};
    int FAYL = açmaq_fayl("시험.txt", oxunan_yazılan | 없으면만들기 | 내용비우기, 0600);
    if (FAYL < 0) return 1;
    if (yazmaq_fayl_verilənlər(FAYL, Məzmun_VALUE, sizeof(Məzmun_VALUE)) != sizeof(Məzmun_VALUE)) return 2;
    if (axtarmaq_fayl(FAYL, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(FAYL, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Məzmun_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Məzmun_VALUE[순번]) return 5;
    if (파일자료읽기(FAYL, 읽은값, 1) != 0) return 6;
    if (파일저장확정(FAYL) != -1 || 오류번호 != 38) return 7;
    if (bağlamaq_fayl(FAYL) || bağlamaq_fayl(FAYL) != -1 || 오류번호 != 9) return 8;
    FAYL = açmaq_fayl("시험.txt", yalnız_oxunan_VALUE);
    if (FAYL < 0 || yazmaq_fayl_verilənlər(FAYL, Məzmun_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (bağlamaq_fayl(FAYL)) return 10;
    FAYL = açmaq_fayl("시험.txt", oxunan_yazılan | 끝에이어쓰기);
    if (FAYL < 0 || axtarmaq_fayl(FAYL, 0, 처음기준) != 0 || yazmaq_fayl_verilənlər(FAYL, "!", 1) != 1 || fayl_ölçünü_dəyişmək(FAYL) != sizeof(Məzmun_VALUE) + 1) return 11;
    if (Dəst_fayl_uzunluq(FAYL, 2) || axtarmaq_fayl(FAYL, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (yazmaq_fayl_verilənlər(FAYL, "x", 1) != 1 || fayl_ölçünü_dəyişmək(FAYL) != 3 || bağlamaq_fayl(FAYL)) return 13;
    FAYL = açmaq_fayl("구멍.bin", oxunan_yazılan | 없으면만들기 | 내용비우기, 0600);
    if (FAYL < 0 || axtarmaq_fayl(FAYL, 3, 처음기준) != 3 || yazmaq_fayl_verilənlər(FAYL, "z", 1) != 1) return 14;
    if (axtarmaq_fayl(FAYL, 0, 처음기준) != 0 || 파일자료읽기(FAYL, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (silmək_fayl_daxiletmə_ad("구멍.bin") || fayl_ölçünü_dəyişmək(FAYL) != 4 || bağlamaq_fayl(FAYL)) return 16;
    if (açmaq_fayl("구멍.bin", yalnız_oxunan_VALUE) != -1 || 오류번호 != 2) return 17;
    if (açmaq_fayl("시험.txt", oxunan_yazılan | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (açmaq_fayl("../금지", yalnız_oxunan_VALUE) != -1) return 19;
    return 0;
}
