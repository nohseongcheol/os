#include "파일규약.h"
class dogfen_rheolwr {
    int INDEX;
public:
    dogfen_rheolwr(const char *Enw) : INDEX(agor_ffeil(Enw, darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600)) {}
    ~dogfen_rheolwr() { if (INDEX >= 0) cau_ffeil(INDEX); }
    입출력결과형 Ysgrifennu(const char *data, beit_COUNT_TYPE Maint) { return ysgrifennu_ffeil_data(INDEX, data, Maint); }
};
extern "C" int START_defnyddiwr_Rhaglen(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dogfen_rheolwr 문서("C++인사.txt");
    ysgrifennu_ffeil_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Ysgrifennu(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
