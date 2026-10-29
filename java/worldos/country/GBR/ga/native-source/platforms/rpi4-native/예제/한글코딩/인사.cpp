#include "파일규약.h"
class doic_bainisteoir {
    int INDEX;
public:
    doic_bainisteoir(const char *Ainm) : INDEX(oscail_comhad(Ainm, inléite_inscríofa | 없으면만들기 | 내용비우기, 0600)) {}
    ~doic_bainisteoir() { if (INDEX >= 0) dún_comhad(INDEX); }
    입출력결과형 Scríobh(const char *sonraí, beart_COUNT_TYPE Méid) { return scríobh_comhad_sonraí(INDEX, sonraí, Méid); }
};
extern "C" int Start_úsáideoir_clár(int Argóintí) {
    (void)Argóintí;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    doic_bainisteoir 문서("C++인사.txt");
    scríobh_comhad_sonraí(1, 인사말, sizeof(인사말) - 1);
    return 문서.Scríobh(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
