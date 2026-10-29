#include "파일규약.h"
class manager_documente {
    int INDEX;
public:
    manager_documente(const char *Nume) : INDEX(crea_Fișier(Nume, citire_scriere | 없으면만들기 | trunchia_TOC, 0600)) {}
    ~manager_documente() { if (INDEX >= 0) închide_Fișier(INDEX); }
    입출력결과형 Scriere(const char *date, byte_COUNT_Tip Mărime) { return scriere_Fișier_date(INDEX, date, Mărime); }
};
extern "C" int buta_utilizator_program(int Argumente) {
    (void)Argumente;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    manager_documente 문서("C++인사.txt");
    scriere_Fișier_date(1, 인사말, sizeof(인사말) - 1);
    return 문서.Scriere(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
