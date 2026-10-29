#include "ABITệp.h"
int bắtChạyChươngTrìnhNgườiDùng(int cácĐốiSố) {
    (void)cácĐốiSố;
    const char lờiChào[] = "C에서 한글 이름과 posix-kor gọiThựcHiện\n";
    int TàiLiệu = mởTệp("C인사.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (TàiLiệu < 0) return 1;
    kiểuKếtQuảVàoRa sốLượngĐãGhi = ghiDữLiệuTệp(TàiLiệu, lờiChào, sizeof(lờiChào) - 1);
    đóngTệp(TàiLiệu);
    ghiDữLiệuTệp(1, lờiChào, sizeof(lờiChào) - 1);
    return sốLượngĐãGhi == sizeof(lờiChào) - 1 ? 0 : 2;
}
