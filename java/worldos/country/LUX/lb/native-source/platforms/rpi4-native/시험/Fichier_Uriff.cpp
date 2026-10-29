#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ Bibliothéik 없는 freestanding C++11 App_f5044b9b. 커널에 statesch_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Inhalt_VALUE[] = "C++ → Java Kernel_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Inhalt_VALUE)] = {};
    int Fichier = ariichten_Fichier("시험.txt", lies_schreiffäeg | 없으면만들기 | 내용비우기, 0600);
    if (Fichier < 0) return 1;
    if (schreiwen_Fichier_Daten(Fichier, Inhalt_VALUE, sizeof(Inhalt_VALUE)) != sizeof(Inhalt_VALUE)) return 2;
    if (sichen_Fichier(Fichier, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fichier, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Inhalt_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Inhalt_VALUE[순번]) return 5;
    if (파일자료읽기(Fichier, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Fichier) != -1 || 오류번호 != 38) return 7;
    if (Clôture_Fichier(Fichier) || Clôture_Fichier(Fichier) != -1 || 오류번호 != 9) return 8;
    Fichier = ariichten_Fichier("시험.txt", schreifgeschützt_VALUE);
    if (Fichier < 0 || schreiwen_Fichier_Daten(Fichier, Inhalt_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (Clôture_Fichier(Fichier)) return 10;
    Fichier = ariichten_Fichier("시험.txt", lies_schreiffäeg | 끝에이어쓰기);
    if (Fichier < 0 || sichen_Fichier(Fichier, 0, 처음기준) != 0 || schreiwen_Fichier_Daten(Fichier, "!", 1) != 1 || Fichier_d_Gréisst_veränneren(Fichier) != sizeof(Inhalt_VALUE) + 1) return 11;
    if (Saz_Fichier_Längt(Fichier, 2) || sichen_Fichier(Fichier, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (schreiwen_Fichier_Daten(Fichier, "x", 1) != 1 || Fichier_d_Gréisst_veränneren(Fichier) != 3 || Clôture_Fichier(Fichier)) return 13;
    Fichier = ariichten_Fichier("구멍.bin", lies_schreiffäeg | 없으면만들기 | 내용비우기, 0600);
    if (Fichier < 0 || sichen_Fichier(Fichier, 3, 처음기준) != 3 || schreiwen_Fichier_Daten(Fichier, "z", 1) != 1) return 14;
    if (sichen_Fichier(Fichier, 0, 처음기준) != 0 || 파일자료읽기(Fichier, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (ewechhuelen_Fichier_Agab_Numm("구멍.bin") || Fichier_d_Gréisst_veränneren(Fichier) != 4 || Clôture_Fichier(Fichier)) return 16;
    if (ariichten_Fichier("구멍.bin", schreifgeschützt_VALUE) != -1 || 오류번호 != 2) return 17;
    if (ariichten_Fichier("시험.txt", lies_schreiffäeg | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (ariichten_Fichier("../금지", schreifgeschützt_VALUE) != -1) return 19;
    return 0;
}
