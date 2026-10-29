#include "파일규약.h"
class skjal_stjórnandi {
    int INDEX;
public:
    skjal_stjórnandi(const char *Heiti) : INDEX(opið_skrá(Heiti, les_skrifheimild | 없으면만들기 | 내용비우기, 0600)) {}
    ~skjal_stjórnandi() { if (INDEX >= 0) loka_skrá(INDEX); }
    입출력결과형 Skrift(const char *gögn, bæti_COUNT_TYPE Stærð) { return skrifa_skrá_gögn(INDEX, gögn, Stærð); }
};
extern "C" int Opna_notandi_forrit(int Viðföng) {
    (void)Viðföng;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    skjal_stjórnandi 문서("C++인사.txt");
    skrifa_skrá_gögn(1, 인사말, sizeof(인사말) - 1);
    return 문서.Skrift(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
