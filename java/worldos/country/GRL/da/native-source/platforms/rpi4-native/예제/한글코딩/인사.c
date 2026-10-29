#include "파일규약.h"
int START_bruger_app(int Argumenter) {
    (void)Argumenter;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = åben_fil("C인사.txt", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = skrive_fil_data(문서, 인사말, sizeof(인사말) - 1);
    Luk_fil(문서);
    skrive_fil_data(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
