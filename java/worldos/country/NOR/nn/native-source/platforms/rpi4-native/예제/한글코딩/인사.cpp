#include "파일규약.h"
class dokument_leiar {
    int INDEX;
public:
    dokument_leiar(const char *Namn) : INDEX(opne_fil(Namn, lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_leiar() { if (INDEX >= 0) Lukk_fil(INDEX); }
    입출력결과형 Skriv(const char *data, byte_COUNT_TYPE Storleik) { return skrive_fil_data(INDEX, data, Storleik); }
};
extern "C" int START_brukar_app(int Argument) {
    (void)Argument;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_leiar 문서("C++인사.txt");
    skrive_fil_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Skriv(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
