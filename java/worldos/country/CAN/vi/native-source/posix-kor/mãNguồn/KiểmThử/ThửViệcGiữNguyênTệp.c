#include <ABITệp.h>
#include <stdio.h>
int main(int sốLượngPhầnMục, char **danhSáchMục) {
    (void)sốLượngPhầnMục; (void)danhSáchMục;
    int Tệp = mởTệp("stored.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (Tệp < 0 || ghiDữLiệuTệp(Tệp, "saved-from-C", 12) != 12) return 1;
    if (lưuTrữTệpChốt(Tệp) < 0) return 2;
    if (đóngTệp(Tệp) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
