#include "파일규약.h"
int BEGIN_gebruiker_program(int 인수) {
    (void)인수;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = skep_lêer("C인사.txt", lees_skryf | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = skryf_lêer_data(문서, 인사말, sizeof(인사말) - 1);
    sluit_lêer(문서);
    skryf_lêer_data(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
