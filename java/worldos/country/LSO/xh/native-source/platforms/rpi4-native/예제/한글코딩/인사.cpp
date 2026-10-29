#include "파일규약.h"
class uxwebhu_umphathi {
    int indeksa;
public:
    uxwebhu_umphathi(const char *Igama) : indeksa(vula_ifayile(Igama, funda_bhala | 없으면만들기 | 내용비우기, 0600)) {}
    ~uxwebhu_umphathi() { if (indeksa >= 0) vala_ifayile(indeksa); }
    입출력결과형 Bhala(const char *iingcombolo, 바이트수형 Ubukhulu) { return bhala_ifayile_iingcombolo(indeksa, iingcombolo, Ubukhulu); }
};
extern "C" int qala_umsebenzisi_inkqubo(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    uxwebhu_umphathi 문서("C++인사.txt");
    bhala_ifayile_iingcombolo(1, 인사말, sizeof(인사말) - 1);
    return 문서.Bhala(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
