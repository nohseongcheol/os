#include "파일규약.h"
int START_korisnik_program(int Argumenti) {
    (void)Argumenti;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = otvoreno_Datoteka("C인사.txt", 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = zapisivanje_Datoteka_podaci(문서, 인사말, sizeof(인사말) - 1);
    Zatvori_Datoteka(문서);
    zapisivanje_Datoteka_podaci(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
