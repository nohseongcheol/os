#include "파일규약.h"
class 문서관리 {
    int INDEX;
public:
    문서관리(const char *Pavadinimas_2) : INDEX(kurti_Failas(Pavadinimas_2, 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600)) {}
    ~문서관리() { if (INDEX >= 0) Uždaryti_Failas(INDEX); }
    입출력결과형 Rašymas(const char *duomenys, baitas_COUNT_TYPE Dydis) { return rašymas_Failas_duomenys(INDEX, duomenys, Dydis); }
};
extern "C" int Start_naudotojas_programa(int Argumentai) {
    (void)Argumentai;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    문서관리 문서("C++인사.txt");
    rašymas_Failas_duomenys(1, 인사말, sizeof(인사말) - 1);
    return 문서.Rašymas(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
