#include "파일규약.h"
int buta_utilizator_program(int Argumente) {
    (void)Argumente;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = crea_Fișier("C인사.txt", citire_scriere | 없으면만들기 | trunchia_TOC, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = scriere_Fișier_date(문서, 인사말, sizeof(인사말) - 1);
    închide_Fișier(문서);
    scriere_Fișier_date(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
