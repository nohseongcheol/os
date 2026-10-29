#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ liburutegi 없는 freestanding C++11 aplik_f5044b9b. 커널에 estatiko_balio 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char eduki_balio[] = "C++ → Java nukleo_balio · 한글 😀";
    unsigned char 읽은값[sizeof(eduki_balio)] = {};
    int Fitxategia = ireki_fitxategi("시험.txt", irakurri_idatzi | 없으면만들기 | 내용비우기, 0600);
    if (Fitxategia < 0) return 1;
    if (idatzi_fitxategi_datuak(Fitxategia, eduki_balio, sizeof(eduki_balio)) != sizeof(eduki_balio)) return 2;
    if (bilatu_fitxategi(Fitxategia, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fitxategia, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(eduki_balio); 순번++) if (읽은값[순번] != (unsigned char)eduki_balio[순번]) return 5;
    if (파일자료읽기(Fitxategia, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fitxategia) != -1 || errorearen_zenbaki != 38) return 7;
    if (itxi_fitxategi(Fitxategia) || itxi_fitxategi(Fitxategia) != -1 || errorearen_zenbaki != 9) return 8;
    Fitxategia = ireki_fitxategi("시험.txt", irakurtzeko_soilik_balio);
    if (Fitxategia < 0 || idatzi_fitxategi_datuak(Fitxategia, eduki_balio, 1) != -1 || errorearen_zenbaki != 9) return 9;
    if (itxi_fitxategi(Fitxategia)) return 10;
    Fitxategia = ireki_fitxategi("시험.txt", irakurri_idatzi | 끝에이어쓰기);
    if (Fitxategia < 0 || bilatu_fitxategi(Fitxategia, 0, 처음기준) != 0 || idatzi_fitxategi_datuak(Fitxategia, "!", 1) != 1 || 파일크기(Fitxategia) != sizeof(eduki_balio) + 1) return 11;
    if (sorta_fitxategi_luzera(Fitxategia, 2) || bilatu_fitxategi(Fitxategia, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (idatzi_fitxategi_datuak(Fitxategia, "x", 1) != 1 || 파일크기(Fitxategia) != 3 || itxi_fitxategi(Fitxategia)) return 13;
    Fitxategia = ireki_fitxategi("구멍.bin", irakurri_idatzi | 없으면만들기 | 내용비우기, 0600);
    if (Fitxategia < 0 || bilatu_fitxategi(Fitxategia, 3, 처음기준) != 3 || idatzi_fitxategi_datuak(Fitxategia, "z", 1) != 1) return 14;
    if (bilatu_fitxategi(Fitxategia, 0, 처음기준) != 0 || 파일자료읽기(Fitxategia, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (kendu_fitxategi_sarrera_izen("구멍.bin") || 파일크기(Fitxategia) != 4 || itxi_fitxategi(Fitxategia)) return 16;
    if (ireki_fitxategi("구멍.bin", irakurtzeko_soilik_balio) != -1 || errorearen_zenbaki != 2) return 17;
    if (ireki_fitxategi("시험.txt", irakurri_idatzi | 새파일만들기, 0600) != -1 || errorearen_zenbaki != 17) return 18;
    if (ireki_fitxategi("../금지", irakurtzeko_soilik_balio) != -1) return 19;
    return 0;
}
