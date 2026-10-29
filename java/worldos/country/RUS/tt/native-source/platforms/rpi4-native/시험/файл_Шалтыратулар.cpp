#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ библиотека 없는 freestanding C++11 кушымта_f5044b9b. 커널에 статик_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Эчтәлек_VALUE[] = "C++ → Java төш_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Эчтәлек_VALUE)] = {};
    int Birem = ачу_файл("시험.txt", укымалы_язмалы | 없으면만들기 | 내용비우기, 0600);
    if (Birem < 0) return 1;
    if (язу_файл_мәгълүмат(Birem, Эчтәлек_VALUE, sizeof(Эчтәлек_VALUE)) != sizeof(Эчтәлек_VALUE)) return 2;
    if (эзләү_файл(Birem, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Birem, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Эчтәлек_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Эчтәлек_VALUE[순번]) return 5;
    if (파일자료읽기(Birem, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Birem) != -1 || 오류번호 != 38) return 7;
    if (чик_файл(Birem) || чик_файл(Birem) != -1 || 오류번호 != 9) return 8;
    Birem = ачу_файл("시험.txt", укымалы_гына_VALUE);
    if (Birem < 0 || язу_файл_мәгълүмат(Birem, Эчтәлек_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (чик_файл(Birem)) return 10;
    Birem = ачу_файл("시험.txt", укымалы_язмалы | 끝에이어쓰기);
    if (Birem < 0 || эзләү_файл(Birem, 0, 처음기준) != 0 || язу_файл_мәгълүмат(Birem, "!", 1) != 1 || файл_үлчәмен_үзгәртү(Birem) != sizeof(Эчтәлек_VALUE) + 1) return 11;
    if (җыелма_файл_озынлык(Birem, 2) || эзләү_файл(Birem, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (язу_файл_мәгълүмат(Birem, "x", 1) != 1 || файл_үлчәмен_үзгәртү(Birem) != 3 || чик_файл(Birem)) return 13;
    Birem = ачу_файл("구멍.bin", укымалы_язмалы | 없으면만들기 | 내용비우기, 0600);
    if (Birem < 0 || эзләү_файл(Birem, 3, 처음기준) != 3 || язу_файл_мәгълүмат(Birem, "z", 1) != 1) return 14;
    if (эзләү_файл(Birem, 0, 처음기준) != 0 || 파일자료읽기(Birem, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (бетерү_файл_кертү_исем("구멍.bin") || файл_үлчәмен_үзгәртү(Birem) != 4 || чик_файл(Birem)) return 16;
    if (ачу_файл("구멍.bin", укымалы_гына_VALUE) != -1 || 오류번호 != 2) return 17;
    if (ачу_файл("시험.txt", укымалы_язмалы | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (ачу_файл("../금지", укымалы_гына_VALUE) != -1) return 19;
    return 0;
}
