#include "파일규약.h"
class dokument_bestuurder {
    int INDEX;
public:
    dokument_bestuurder(const char *Naam) : INDEX(skep_lêer(Naam, lees_skryf | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_bestuurder() { if (INDEX >= 0) sluit_lêer(INDEX); }
    입출력결과형 Skryf(const char *data, greep_COUNT_TYPE Grootte) { return skryf_lêer_data(INDEX, data, Grootte); }
};
extern "C" int BEGIN_gebruiker_program(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_bestuurder 문서("C++인사.txt");
    skryf_lêer_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Skryf(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
