#include "파일규약.h"
int huɓɓude_kuutoro_tafirde(int 인수) {
    (void)인수;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = udditde_fiilde("C인사.txt", tar_winndu | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = winndude_fiilde_keɓe(문서, 인사말, sizeof(인사말) - 1);
    uddude_fiilde(문서);
    winndude_fiilde_keɓe(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
