#include "ABIMạng.h"

int bắtChạyChươngTrìnhNgườiDùng(int cácĐốiSố) {
    (void)cácĐốiSố;
    struct ĐịaChỉỔCắmMạngLiênMạng địaChỉ = {0};
    địaChỉ.họĐịaChỉ = HọLiênMạng;
    địaChỉ.sốCổng = ngắnKiểuMạng(9260);
    địaChỉ.ĐịaChỉLiênMạng.giáTrịĐịaChỉ = sốNguyênMạng(địaChỉVòngVề);
    int giáTrịMáyChủ = tạoĐiểmCuối(HọLiênMạng, MạngLuồng, giaoThứcVậnChuyểnLuồng);
    if (giáTrịMáyChủ < 0 || ràngBuộcĐịaChỉ(giáTrịMáyChủ, (struct ĐịaChỉỔCắmMạng *)&địaChỉ, sizeof(địaChỉ)) < 0 ||
        chờKếtNốiMạngCho(giáTrịMáyChủ, 4) < 0) return 1;
    if (chấpNhậnKếtNốiMạng(giáTrịMáyChủ, 0, 0) != -1 || sốLỗi != 11) return 2;
    int giáTrịKhách = tạoĐiểmCuối(HọLiênMạng, MạngLuồng, giaoThứcVậnChuyểnLuồng);
    if (giáTrịKhách < 0 || kếtNốiMạng(giáTrịKhách, (struct ĐịaChỉỔCắmMạng *)&địaChỉ, sizeof(địaChỉ)) < 0) return 3;
    int nốiKết = chấpNhậnKếtNốiMạng(giáTrịMáyChủ, 0, 0);
    if (nốiKết < 0) return 4;
    unsigned char gửiĐếnPhầnMục[1500], phầnMụcĐãNhận[1500];
    for (int trịSố = 0; trịSố < 1500; trịSố++) gửiĐếnPhầnMục[trịSố] = (unsigned char)trịSố;
    int sốLượngĐãGửi = 0;
    while (sốLượngĐãGửi < 1024) {
        int độDài = ghiDữLiệuTệp(giáTrịKhách, gửiĐếnPhầnMục + sốLượngĐãGửi, sizeof(gửiĐếnPhầnMục) - sốLượngĐãGửi);
        if (độDài <= 0) return 5;
        sốLượngĐãGửi += độDài;
    }
    if (ghiDữLiệuTệp(giáTrịKhách, gửiĐếnPhầnMục, 1) != -1 || sốLỗi != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 xâyDựngTấtCả 읽은 giáTrịLùi EOF가 된다. */
    đóngTệp(giáTrịKhách);
    int sốLượngĐãNhận = 0;
    while (sốLượngĐãNhận < sốLượngĐãGửi) {
        int độDài = đọcDữLiệuTệp(nốiKết, phầnMụcĐãNhận + sốLượngĐãNhận, sizeof(phầnMụcĐãNhận) - sốLượngĐãNhận);
        if (độDài <= 0) return 7;
        sốLượngĐãNhận += độDài;
    }
    for (int trịSố = 0; trịSố < sốLượngĐãNhận; trịSố++) if (phầnMụcĐãNhận[trịSố] != gửiĐếnPhầnMục[trịSố]) return 8;
    if (đọcDữLiệuTệp(nốiKết, phầnMụcĐãNhận, 1) != 0) return 9;
    if (ghiDữLiệuTệp(nốiKết, gửiĐếnPhầnMục, 1) != -1 || sốLỗi != 32) return 10;
    đóngTệp(nốiKết); đóngTệp(giáTrịMáyChủ);
    const char kếtQuả[] = "C posix-kor 연결형 TruyềnThông PASS\n";
    ghiDữLiệuTệp(1, kếtQuả, sizeof(kếtQuả) - 1);
    return 0;
}
