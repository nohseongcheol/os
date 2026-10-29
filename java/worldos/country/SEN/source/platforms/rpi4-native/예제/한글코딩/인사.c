#include "파일규약.h"
int Door_kiy_jariñoo_internet_jëfekaay(int 인수) {
    (void)인수;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = sos_bara_denc("C인사.txt", jàng_bind | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = biir_bara_denc_mbir(문서, 인사말, sizeof(인사말) - 1);
    Tej_bara_denc(문서);
    biir_bara_denc_mbir(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
