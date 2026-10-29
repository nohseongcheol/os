#include "파일규약.h"
class dokument_iş_dolandyryjy {
    int indeks;
public:
    dokument_iş_dolandyryjy(const char *Ad) : indeks(aç_faýl(Ad, okalýan_ýazylýan | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_iş_dolandyryjy() { if (indeks >= 0) ýap_faýl(indeks); }
    입출력결과형 Ýaz(const char *maglumat, 바이트수형 Ululyk) { return ýaz_faýl_maglumat(indeks, maglumat, Ululyk); }
};
extern "C" int başlat_ulanyjy_programma(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_iş_dolandyryjy 문서("C++인사.txt");
    ýaz_faýl_maglumat(1, 인사말, sizeof(인사말) - 1);
    return 문서.Ýaz(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
