#include "파일규약.h"
class àkọsílẹ̀_alákòóso {
    int wá_atọ̀ka_àkóónú;
public:
    àkọsílẹ̀_alákòóso(const char *Orúkọ) : wá_atọ̀ka_àkóónú(ṣí_fáìlì(Orúkọ, tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600)) {}
    ~àkọsílẹ̀_alákòóso() { if (wá_atọ̀ka_àkóónú >= 0) pa_dé_fáìlì(wá_atọ̀ka_àkóónú); }
    입출력결과형 Kọ(const char *détà, 바이트수형 Ìwọ̀n) { return kọ_fáìlì_détà(wá_atọ̀ka_àkóónú, détà, Ìwọ̀n); }
};
extern "C" int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    àkọsílẹ̀_alákòóso 문서("C++인사.txt");
    kọ_fáìlì_détà(1, 인사말, sizeof(인사말) - 1);
    return 문서.Kọ(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
