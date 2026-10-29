#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ Kitaphana 없는 freestanding C++11 programma_f5044b9b. 커널에 statiki_baha 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Mazmun_baha[] = "C++ → Java ýadro_baha · 한글 😀";
    unsigned char 읽은값[sizeof(Mazmun_baha)] = {};
    int Faýl = aç_faýl("시험.txt", okalýan_ýazylýan | 없으면만들기 | 내용비우기, 0600);
    if (Faýl < 0) return 1;
    if (ýaz_faýl_maglumat(Faýl, Mazmun_baha, sizeof(Mazmun_baha)) != sizeof(Mazmun_baha)) return 2;
    if (gözle_faýl(Faýl, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Faýl, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Mazmun_baha); 순번++) if (읽은값[순번] != (unsigned char)Mazmun_baha[순번]) return 5;
    if (파일자료읽기(Faýl, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Faýl) != -1 || 오류번호 != 38) return 7;
    if (ýap_faýl(Faýl) || ýap_faýl(Faýl) != -1 || 오류번호 != 9) return 8;
    Faýl = aç_faýl("시험.txt", diňe_okalýan_baha);
    if (Faýl < 0 || ýaz_faýl_maglumat(Faýl, Mazmun_baha, 1) != -1 || 오류번호 != 9) return 9;
    if (ýap_faýl(Faýl)) return 10;
    Faýl = aç_faýl("시험.txt", okalýan_ýazylýan | 끝에이어쓰기);
    if (Faýl < 0 || gözle_faýl(Faýl, 0, 처음기준) != 0 || ýaz_faýl_maglumat(Faýl, "!", 1) != 1 || faýl_ölçegi_üýtget(Faýl) != sizeof(Mazmun_baha) + 1) return 11;
    if (köplük_faýl_dowamlylyk(Faýl, 2) || gözle_faýl(Faýl, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (ýaz_faýl_maglumat(Faýl, "x", 1) != 1 || faýl_ölçegi_üýtget(Faýl) != 3 || ýap_faýl(Faýl)) return 13;
    Faýl = aç_faýl("구멍.bin", okalýan_ýazylýan | 없으면만들기 | 내용비우기, 0600);
    if (Faýl < 0 || gözle_faýl(Faýl, 3, 처음기준) != 3 || ýaz_faýl_maglumat(Faýl, "z", 1) != 1) return 14;
    if (gözle_faýl(Faýl, 0, 처음기준) != 0 || 파일자료읽기(Faýl, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (aýyr_faýl_girizmeklik_at("구멍.bin") || faýl_ölçegi_üýtget(Faýl) != 4 || ýap_faýl(Faýl)) return 16;
    if (aç_faýl("구멍.bin", diňe_okalýan_baha) != -1 || 오류번호 != 2) return 17;
    if (aç_faýl("시험.txt", okalýan_ýazylýan | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (aç_faýl("../금지", diňe_okalýan_baha) != -1) return 19;
    return 0;
}
