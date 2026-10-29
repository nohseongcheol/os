#include "파일규약.h"
class dokumen_pengurus {
    int INDEX;
public:
    dokumen_pengurus(const char *Nama) : INDEX(buka_fail(Nama, baca_tulis | 없으면만들기 | potong_TOC, 0600)) {}
    ~dokumen_pengurus() { if (INDEX >= 0) Tutup_fail(INDEX); }
    입출력결과형 Tulis(const char *data, bait_COUNT_TYPE Saiz) { return tulis_fail_data(INDEX, data, Saiz); }
};
extern "C" int Mula_pengguna_aplikasi(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokumen_pengurus 문서("C++인사.txt");
    tulis_fail_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Tulis(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
