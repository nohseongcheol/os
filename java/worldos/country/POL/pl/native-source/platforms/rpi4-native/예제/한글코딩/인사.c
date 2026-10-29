#include "Plik_ABI.h"
int START_użytkownik_program(int argumenty) {
    (void)argumenty;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = otwarty_Plik("C인사.txt", R_W | 없으면만들기 | obcinać_Spis_treści, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = zapis_Plik_dane(문서, 인사말, sizeof(인사말) - 1);
    Zamknij_Plik(문서);
    zapis_Plik_dane(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
