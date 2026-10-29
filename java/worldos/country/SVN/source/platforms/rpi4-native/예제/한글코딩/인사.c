#include "파일규약.h"
int Start_uporabnik_aplikacija(int Argumenti) {
    (void)Argumenti;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = odprto_Datoteka("C인사.txt", branje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = pisati_Datoteka_podatki(문서, 인사말, sizeof(인사말) - 1);
    Zapri_Datoteka(문서);
    pisati_Datoteka_podatki(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
