#include "파일규약.h"
int Start_naudotojas_programa(int Argumentai) {
    (void)Argumentai;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = kurti_Failas("C인사.txt", 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = rašymas_Failas_duomenys(문서, 인사말, sizeof(인사말) - 1);
    Uždaryti_Failas(문서);
    rašymas_Failas_duomenys(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
