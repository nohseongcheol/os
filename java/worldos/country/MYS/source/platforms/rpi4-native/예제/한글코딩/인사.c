#include "파일규약.h"
int Mula_pengguna_aplikasi(int 인수) {
    (void)인수;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = buka_fail("C인사.txt", baca_tulis | 없으면만들기 | potong_TOC, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = tulis_fail_data(문서, 인사말, sizeof(인사말) - 1);
    Tutup_fail(문서);
    tulis_fail_data(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
