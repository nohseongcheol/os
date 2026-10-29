#include "파일규약.h"
int START_brukar_app(int Argument) {
    (void)Argument;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = opne_fil("C인사.txt", lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = skrive_fil_data(문서, 인사말, sizeof(인사말) - 1);
    Lukk_fil(문서);
    skrive_fil_data(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
