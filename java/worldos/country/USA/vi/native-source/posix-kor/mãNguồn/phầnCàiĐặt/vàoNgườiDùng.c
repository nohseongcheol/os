#include "RanhGiớiGọi.h"
extern int main(int sốLượngCácĐốiSố, char **danhSáchĐốiSố);
static char bộNhớĐốiSố[2048];
static char *danhSáchĐốiSố[18];
int jkoros_main(void) {
    int sốLượngPhầnMục = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (sốLượngPhầnMục < 0 || sốLượngPhầnMục > 16) return 126;
    /* phầnMụcHiệnTại 커널의 argv는 thựcThiLệnh 이름을 제외한다. C argv[0]은 고정 nhậnDạngGiáTrị 이름이다. */
    danhSáchĐốiSố[0] = "jkoros-app";
    int vịTrí = 0;
    for (int sốHiệu = 0; sốHiệu < sốLượngPhầnMục; sốHiệu++) {
        const int *nguyênBản = (const int *)jkoros_syscall(3, sốHiệu, 0, 0, 0, 0);
        if (!nguyênBản || nguyênBản[0] < 0 || nguyênBản[0] > 127) return 126;
        danhSáchĐốiSố[sốHiệu + 1] = bộNhớĐốiSố + vịTrí;
        for (int mụcÔ = 0; mụcÔ < nguyênBản[0]; mụcÔ++) {
            if (vịTrí >= 2047) return 126;
            bộNhớĐốiSố[vịTrí++] = nguyênBản[mụcÔ + 1];
        }
        bộNhớĐốiSố[vịTrí++] = 0;
    }
    danhSáchĐốiSố[sốLượngPhầnMục + 1] = 0;
    return main(sốLượngPhầnMục + 1, danhSáchĐốiSố);
}
