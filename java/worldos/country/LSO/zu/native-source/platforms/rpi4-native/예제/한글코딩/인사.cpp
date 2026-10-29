#include "파일규약.h"
class umqulu_imeneja {
    int thola_inkomba;
public:
    umqulu_imeneja(const char *Igama) : thola_inkomba(vula_ifayela(Igama, fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600)) {}
    ~umqulu_imeneja() { if (thola_inkomba >= 0) vala_ifayela(thola_inkomba); }
    입출력결과형 Bhala(const char *imininingwane, 바이트수형 Ubungako) { return bhala_ifayela_imininingwane(thola_inkomba, imininingwane, Ubungako); }
};
extern "C" int qala_umsebenzisi_i_app(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    umqulu_imeneja 문서("C++인사.txt");
    bhala_ifayela_imininingwane(1, 인사말, sizeof(인사말) - 1);
    return 문서.Bhala(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
