#include "파일규약.h"
int START_používateľ_program(int Argumenty) {
    (void)Argumenty;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = otvoriť_Súbor("C인사.txt", na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = zapísať_Súbor_údaje(문서, 인사말, sizeof(인사말) - 1);
    Zavrieť_Súbor(문서);
    zapísať_Súbor_údaje(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
