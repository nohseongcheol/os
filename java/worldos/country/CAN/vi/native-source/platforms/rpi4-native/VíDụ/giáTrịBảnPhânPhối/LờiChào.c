#include <ABITệp.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int sốLượngCácĐốiSố, char **danhSáchĐốiSố) {
    if (sốLượngCácĐốiSố < 1 || !danhSáchĐốiSố[0]) return 2;
    const char lờiChào[] = "tựThân 커널의 C와 tiếngViệt POSIX\n";
    int TàiLiệu = mởTệp("LờiChào.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (TàiLiệu < 0) return 1;
    kiểuKếtQuảVàoRa độDài = ghiDữLiệuTệp(TàiLiệu, lờiChào, sizeof(lờiChào) - 1);
    đóngTệp(TàiLiệu);
    ghiDữLiệuTệp(1, lờiChào, sizeof(lờiChào) - 1);
    return độDài == sizeof(lờiChào) - 1 ? 0 : 3;
}
