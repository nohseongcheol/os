#include "파일규약.h"
int Başla_istifadəçi_proqram(int 인수) {
    (void)인수;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = açmaq_fayl("C인사.txt", oxunan_yazılan | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = yazmaq_fayl_verilənlər(문서, 인사말, sizeof(인사말) - 1);
    bağlamaq_fayl(문서);
    yazmaq_fayl_verilənlər(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
