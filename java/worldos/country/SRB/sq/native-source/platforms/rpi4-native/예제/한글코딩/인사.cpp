#include "파일규약.h"
class dokument_menaxher {
    int INDEX;
public:
    dokument_menaxher(const char *Emër) : INDEX(hap_skedar(Emër, lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_menaxher() { if (INDEX >= 0) mbyll_skedar(INDEX); }
    입출력결과형 Shkrimi(const char *të_dhëna, bajt_COUNT_TYPE Madhësi) { return shkruaj_skedar_të_dhëna(INDEX, të_dhëna, Madhësi); }
};
extern "C" int nis_përdorues_program(int Argumente) {
    (void)Argumente;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_menaxher 문서("C++인사.txt");
    shkruaj_skedar_të_dhëna(1, 인사말, sizeof(인사말) - 1);
    return 문서.Shkrimi(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
