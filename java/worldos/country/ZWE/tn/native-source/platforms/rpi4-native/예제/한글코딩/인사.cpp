#include "파일규약.h"
class Tokumente_motsamaisi {
    int tshupane;
public:
    Tokumente_motsamaisi(const char *leina) : tshupane(bula_faele(leina, buisa_kwala | 없으면만들기 | 내용비우기, 0600)) {}
    ~Tokumente_motsamaisi() { if (tshupane >= 0) tswala_faele(tshupane); }
    입출력결과형 kwala(const char *tshedimosetso, 바이트수형 lekanya) { return kwala_faele_tshedimosetso(tshupane, tshedimosetso, lekanya); }
};
extern "C" int simolola_modirisi_Tiriso(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    Tokumente_motsamaisi 문서("C++인사.txt");
    kwala_faele_tshedimosetso(1, 인사말, sizeof(인사말) - 1);
    return 문서.kwala(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
