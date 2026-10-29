#include "파일규약.h"
class daftarin_aiki_Manaja {
    int Indes;
public:
    daftarin_aiki_Manaja(const char *Suna) : Indes(buɗe_Fayil(Suna, Rubutuwa_karantuwa | 없으면만들기 | 내용비우기, 0600)) {}
    ~daftarin_aiki_Manaja() { if (Indes >= 0) Rufe_Fayil(Indes); }
    입출력결과형 Yi_Rubutu(const char *Tarin_bayani, 바이트수형 Girma) { return Rubuta_Fayil_Tarin_bayani(Indes, Tarin_bayani, Girma); }
};
extern "C" int Fara_Mai_anfani_da_kwamfuta_Shiri(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    daftarin_aiki_Manaja 문서("C++인사.txt");
    Rubuta_Fayil_Tarin_bayani(1, 인사말, sizeof(인사말) - 1);
    return 문서.Yi_Rubutu(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
