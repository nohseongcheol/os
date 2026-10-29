#include "파일규약.h"
class titiqqaq_aulattiji {
    int nalunaiqsimavik;
public:
    titiqqaq_aulattiji(const char *atiq) : nalunaiqsimavik(matuirli_ini(atiq, uqalimaarli_titirarli | 없으면만들기 | 내용비우기, 0600)) {}
    ~titiqqaq_aulattiji() { if (nalunaiqsimavik >= 0) matuli_ini(nalunaiqsimavik); }
    입출력결과형 titiraq(const char *titiqqat, 바이트수형 anininga) { return titiraq_ini_titiqqat(nalunaiqsimavik, titiqqat, anininga); }
};
extern "C" int pigiarli_atuqtuq_pilirijjut(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    titiqqaq_aulattiji 문서("C++인사.txt");
    titiraq_ini_titiqqat(1, 인사말, sizeof(인사말) - 1);
    return 문서.titiraq(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
