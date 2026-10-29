#include "ABITệp.h"
class BộQuảnLýTàiLiệu {
    int sốHiệu;
public:
    BộQuảnLýTàiLiệu(const char *tên) : sốHiệu(mởTệp(tên, GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600)) {}
    ~BộQuảnLýTàiLiệu() { if (sốHiệu >= 0) đóngTệp(sốHiệu); }
    kiểuKếtQuảVàoRa ghi(const char *DữLiệu, kiểuSốLượngByte cỡ) { return ghiDữLiệuTệp(sốHiệu, DữLiệu, cỡ); }
};
extern "C" int bắtChạyChươngTrìnhNgườiDùng(int cácĐốiSố) {
    (void)cácĐốiSố;
    const char lờiChào[] = "C++에서 한글 클래스와 posix-kor gọiThựcHiện\n";
    BộQuảnLýTàiLiệu TàiLiệu("C++LờiChào.txt");
    ghiDữLiệuTệp(1, lờiChào, sizeof(lờiChào) - 1);
    return TàiLiệu.ghi(lờiChào, sizeof(lờiChào) - 1) == sizeof(lờiChào) - 1 ? 0 : 1;
}
