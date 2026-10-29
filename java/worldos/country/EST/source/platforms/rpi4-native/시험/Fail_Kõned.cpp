#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ teek 없는 freestanding C++11 programm_f5044b9b. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Sisu_VALUE[] = "C++ → Java tuum_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Sisu_VALUE)] = {};
    int Fail = avama_Fail("시험.txt", 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600);
    if (Fail < 0) return 1;
    if (kirjutamine_Fail_andmed(Fail, Sisu_VALUE, sizeof(Sisu_VALUE)) != sizeof(Sisu_VALUE)) return 2;
    if (otsima_Fail(Fail, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fail, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Sisu_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Sisu_VALUE[순번]) return 5;
    if (파일자료읽기(Fail, 읽은값, 1) != 0) return 6;
    if (kinnitamine_failisalvestusruum(Fail) != -1 || tõrke_number != 38) return 7;
    if (Sule_Fail(Fail) || Sule_Fail(Fail) != -1 || tõrke_number != 9) return 8;
    Fail = avama_Fail("시험.txt", kirjutuskaitstud_VALUE);
    if (Fail < 0 || kirjutamine_Fail_andmed(Fail, Sisu_VALUE, 1) != -1 || tõrke_number != 9) return 9;
    if (Sule_Fail(Fail)) return 10;
    Fail = avama_Fail("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (Fail < 0 || otsima_Fail(Fail, 0, 처음기준) != 0 || kirjutamine_Fail_andmed(Fail, "!", 1) != 1 || faili_maht(Fail) != sizeof(Sisu_VALUE) + 1) return 11;
    if (파일길이정하기(Fail, 2) || otsima_Fail(Fail, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (kirjutamine_Fail_andmed(Fail, "x", 1) != 1 || faili_maht(Fail) != 3 || Sule_Fail(Fail)) return 13;
    Fail = avama_Fail("구멍.bin", 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600);
    if (Fail < 0 || otsima_Fail(Fail, 3, 처음기준) != 3 || kirjutamine_Fail_andmed(Fail, "z", 1) != 1) return 14;
    if (otsima_Fail(Fail, 0, 처음기준) != 0 || 파일자료읽기(Fail, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (eemaldama_Fail_kirje_nimetus("구멍.bin") || faili_maht(Fail) != 4 || Sule_Fail(Fail)) return 16;
    if (avama_Fail("구멍.bin", kirjutuskaitstud_VALUE) != -1 || tõrke_number != 2) return 17;
    if (avama_Fail("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || tõrke_number != 17) return 18;
    if (avama_Fail("../금지", kirjutuskaitstud_VALUE) != -1) return 19;
    return 0;
}
