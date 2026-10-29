#include "파일규약.h"
class Dok_Manager {
    int INDEX;
public:
    Dok_Manager(const char *Numm) : INDEX(ariichten_Fichier(Numm, lies_schreiffäeg | 없으면만들기 | 내용비우기, 0600)) {}
    ~Dok_Manager() { if (INDEX >= 0) Clôture_Fichier(INDEX); }
    입출력결과형 schreiwen(const char *Daten, Byte_COUNT_TYPE d_Gréisst_veränneren) { return schreiwen_Fichier_Daten(INDEX, Daten, d_Gréisst_veränneren); }
};
extern "C" int Start_Benotzer_App(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    Dok_Manager 문서("C++인사.txt");
    schreiwen_Fichier_Daten(1, 인사말, sizeof(인사말) - 1);
    return 문서.schreiwen(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
