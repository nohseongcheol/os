#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ isomero 없는 freestanding C++11 porogaramu_f5044b9b. 커널에 kitayega_agaciro 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Ibirimo_agaciro[] = "C++ → Java intima_agaciro · 한글 😀";
    unsigned char 읽은값[sizeof(Ibirimo_agaciro)] = {};
    int Idosiye = kurema_dosiye("시험.txt", gusoma_kwandika | 없으면만들기 | 내용비우기, 0600);
    if (Idosiye < 0) return 1;
    if (kwandika_dosiye_amakurushingiro(Idosiye, Ibirimo_agaciro, sizeof(Ibirimo_agaciro)) != sizeof(Ibirimo_agaciro)) return 2;
    if (파일위치옮기기(Idosiye, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Idosiye, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Ibirimo_agaciro); 순번++) if (읽은값[순번] != (unsigned char)Ibirimo_agaciro[순번]) return 5;
    if (파일자료읽기(Idosiye, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Idosiye) != -1 || 오류번호 != 38) return 7;
    if (gufunga_dosiye(Idosiye) || gufunga_dosiye(Idosiye) != -1 || 오류번호 != 9) return 8;
    Idosiye = kurema_dosiye("시험.txt", soma_gusa_agaciro);
    if (Idosiye < 0 || kwandika_dosiye_amakurushingiro(Idosiye, Ibirimo_agaciro, 1) != -1 || 오류번호 != 9) return 9;
    if (gufunga_dosiye(Idosiye)) return 10;
    Idosiye = kurema_dosiye("시험.txt", gusoma_kwandika | 끝에이어쓰기);
    if (Idosiye < 0 || 파일위치옮기기(Idosiye, 0, 처음기준) != 0 || kwandika_dosiye_amakurushingiro(Idosiye, "!", 1) != 1 || dosiye_ingano(Idosiye) != sizeof(Ibirimo_agaciro) + 1) return 11;
    if (itsinda_dosiye_uburebure(Idosiye, 2) || 파일위치옮기기(Idosiye, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (kwandika_dosiye_amakurushingiro(Idosiye, "x", 1) != 1 || dosiye_ingano(Idosiye) != 3 || gufunga_dosiye(Idosiye)) return 13;
    Idosiye = kurema_dosiye("구멍.bin", gusoma_kwandika | 없으면만들기 | 내용비우기, 0600);
    if (Idosiye < 0 || 파일위치옮기기(Idosiye, 3, 처음기준) != 3 || kwandika_dosiye_amakurushingiro(Idosiye, "z", 1) != 1) return 14;
    if (파일위치옮기기(Idosiye, 0, 처음기준) != 0 || 파일자료읽기(Idosiye, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (gukuramo_dosiye_icyinjizwa_izina("구멍.bin") || dosiye_ingano(Idosiye) != 4 || gufunga_dosiye(Idosiye)) return 16;
    if (kurema_dosiye("구멍.bin", soma_gusa_agaciro) != -1 || 오류번호 != 2) return 17;
    if (kurema_dosiye("시험.txt", gusoma_kwandika | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (kurema_dosiye("../금지", soma_gusa_agaciro) != -1) return 19;
    return 0;
}
