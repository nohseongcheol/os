#include "파일규약.h"
class 문서관리 {
    int INDEX;
public:
    문서관리(const char *Názov) : INDEX(otvoriť_Súbor(Názov, na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600)) {}
    ~문서관리() { if (INDEX >= 0) Zavrieť_Súbor(INDEX); }
    입출력결과형 Zápis(const char *údaje, Byte_COUNT_Typ Veľkosť) { return zapísať_Súbor_údaje(INDEX, údaje, Veľkosť); }
};
extern "C" int START_používateľ_program(int Argumenty) {
    (void)Argumenty;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    문서관리 문서("C++인사.txt");
    zapísať_Súbor_údaje(1, 인사말, sizeof(인사말) - 1);
    return 문서.Zápis(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
