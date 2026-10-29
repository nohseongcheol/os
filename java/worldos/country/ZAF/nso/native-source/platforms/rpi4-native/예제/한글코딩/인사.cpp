#include "파일규약.h"
class tokumente_molaodi {
    int lokela;
public:
    tokumente_molaodi(const char *Leina) : lokela(bula_faele(Leina, bala_ngwala | 없으면만들기 | 내용비우기, 0600)) {}
    ~tokumente_molaodi() { if (lokela >= 0) tswalela_faele(lokela); }
    입출력결과형 Ngwala(const char *data, 바이트수형 Bogolo) { return ngwala_faele_data(lokela, data, Bogolo); }
};
extern "C" int Thomišo_mošomiši_tirišo(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    tokumente_molaodi 문서("C++인사.txt");
    ngwala_faele_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Ngwala(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
