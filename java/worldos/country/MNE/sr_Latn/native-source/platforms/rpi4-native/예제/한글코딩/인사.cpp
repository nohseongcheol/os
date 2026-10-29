#include "파일규약.h"
class dokument_menadžer {
    int INDEX;
public:
    dokument_menadžer(const char *ime) : INDEX(otvoren_Datoteka(ime, za_čitanje_pisanje | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_menadžer() { if (INDEX >= 0) Zatvori_Datoteka(INDEX); }
    입출력결과형 쓰기(const char *podaci, bajt_COUNT_tip promeniti_veličinu) { return 파일자료쓰기(INDEX, podaci, promeniti_veličinu); }
};
extern "C" int START_korisnik_program(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_menadžer 문서("C++인사.txt");
    파일자료쓰기(1, 인사말, sizeof(인사말) - 1);
    return 문서.쓰기(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
