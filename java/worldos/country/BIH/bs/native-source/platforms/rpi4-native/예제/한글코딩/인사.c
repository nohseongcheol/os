#include "파일규약.h"
int START_korisnik_program(int Argumenti) {
    (void)Argumenti;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = kreirati_fajl("C인사.txt", i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = pisati_fajl_podaci(문서, 인사말, sizeof(인사말) - 1);
    zatvoriti_fajl(문서);
    pisati_fajl_podaci(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
