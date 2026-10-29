#include "파일규약.h"
int Opna_notandi_forrit(int Viðföng) {
    (void)Viðföng;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = opið_skrá("C인사.txt", les_skrifheimild | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = skrifa_skrá_gögn(문서, 인사말, sizeof(인사말) - 1);
    loka_skrá(문서);
    skrifa_skrá_gögn(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
