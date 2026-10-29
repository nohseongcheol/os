#include "파일규약.h"
class warak_msimamizi {
    int kielezo;
public:
    warak_msimamizi(const char *Jina) : kielezo(unda_faili(Jina, soma_andika | 없으면만들기 | 내용비우기, 0600)) {}
    ~warak_msimamizi() { if (kielezo >= 0) funga_faili(kielezo); }
    입출력결과형 andika(const char *data, 바이트수형 panga_ukubwa) { return andika_faili_data(kielezo, data, panga_ukubwa); }
};
extern "C" int Anza_mtumiaji_programu(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    warak_msimamizi 문서("C++인사.txt");
    andika_faili_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.andika(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
