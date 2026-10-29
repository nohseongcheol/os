#include "파일규약.h"
int START_gebruiker_app(int argumenten) {
    (void)argumenten;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int Guides = open_Bestand("C인사.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (Guides < 0) return 1;
    입출력결과형 기록한수 = schrijven_Bestand_gegevens(Guides, 인사말, sizeof(인사말) - 1);
    Sluiten_Bestand(Guides);
    schrijven_Bestand_gegevens(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
