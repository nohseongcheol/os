#include "파일규약.h"
int Fara_Mai_anfani_da_kwamfuta_Shiri(int 인수) {
    (void)인수;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = buɗe_Fayil("C인사.txt", Rubutuwa_karantuwa | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = Rubuta_Fayil_Tarin_bayani(문서, 인사말, sizeof(인사말) - 1);
    Rufe_Fayil(문서);
    Rubuta_Fayil_Tarin_bayani(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
