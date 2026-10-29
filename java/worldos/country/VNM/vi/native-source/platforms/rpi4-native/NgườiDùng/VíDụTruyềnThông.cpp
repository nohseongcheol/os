#include "ABIMạng.h"
static ĐịaChỉỔCắmMạngLiênMạng địaChỉ(unsigned giáTrịCổng) {
    ĐịaChỉỔCắmMạngLiênMạng giáTrị = {}; giáTrị.họĐịaChỉ = HọLiênMạng;
    giáTrị.sốCổng = ngắnKiểuMạng(giáTrịCổng); giáTrị.ĐịaChỉLiênMạng.giáTrịĐịaChỉ = sốNguyênMạng(địaChỉVòngVề); return giáTrị;
}
extern "C" int bắtChạyChươngTrìnhNgườiDùng(int) {
    int điểmCuốiĐangGửi = tạoĐiểmCuối(HọLiênMạng, ỔCắmMạngĐiệnDữLiệu, 0);
    int điểmCuốiBộNhận = tạoĐiểmCuối(HọLiênMạng, ỔCắmMạngĐiệnDữLiệu, GiaoThứcĐiệnDữLiệu);
    if (điểmCuốiĐangGửi < 0 || điểmCuốiBộNhận < 0) return 1;
    ĐịaChỉỔCắmMạngLiênMạng giáTrịĐến = địaChỉ(7777), giáTrịRờiĐi = địaChỉ(7778), địaChỉĐãGửi = {};
    kiểuĐộDàiĐịaChỉỔCắmMạng độDàiĐịaChỉ = sizeof(địaChỉĐãGửi);
    if (ràngBuộcĐịaChỉ(điểmCuốiBộNhận, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến))) return 2;
    if (ràngBuộcĐịaChỉ(điểmCuốiĐangGửi, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến)) != -1 || sốLỗi != 98) return 3;
    if (ràngBuộcĐịaChỉ(điểmCuốiĐangGửi, (ĐịaChỉỔCắmMạng *)&giáTrịRờiĐi, sizeof(giáTrịRờiĐi))) return 4;
    static const char giáTrịNộiDung[] = "한글 UDP loopback 😀";
    char giáTrịĐãNhận[64] = {};
    if (gửiDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, giáTrịNộiDung, sizeof(giáTrịNộiDung), 0, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến)) != sizeof(giáTrịNộiDung)) return 5;
    if (nhậnDữLiệuĐiệnDữLiệu(điểmCuốiBộNhận, (void *)giáTrịNộiDung, sizeof(giáTrịNộiDung), 0, 0, 0) != -1 || sốLỗi != 14) return 6;
    if (nhậnDữLiệuĐiệnDữLiệu(điểmCuốiBộNhận, giáTrịĐãNhận, sizeof(giáTrịĐãNhận), 0, (ĐịaChỉỔCắmMạng *)&địaChỉĐãGửi, &độDàiĐịaChỉ) != sizeof(giáTrịNộiDung)) return 7;
    if (độDàiĐịaChỉ != sizeof(địaChỉĐãGửi) || ngắnKiểuThứTựThiếtBị(địaChỉĐãGửi.sốCổng) != 7778 || sốNguyênThứTựThiếtBị(địaChỉĐãGửi.ĐịaChỉLiênMạng.giáTrịĐịaChỉ) != địaChỉVòngVề) return 8;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sizeof(giáTrịNộiDung); chỉSốThứBậc++) if (giáTrịĐãNhận[chỉSốThứBậc] != giáTrịNộiDung[chỉSốThứBậc]) return 9;
    if (nhậnDữLiệuĐiệnDữLiệu(điểmCuốiBộNhận, giáTrịĐãNhận, sizeof(giáTrịĐãNhận), 0, 0, 0) != -1 || sốLỗi != 11) return 10;
    if (gửiDữLiệuĐiệnDữLiệu(điểmCuốiBộNhận, giáTrịĐãNhận, sizeof(giáTrịNộiDung), 0, (ĐịaChỉỔCắmMạng *)&địaChỉĐãGửi, sizeof(địaChỉĐãGửi)) != sizeof(giáTrịNộiDung)) return 11;
    if (nhậnDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, giáTrịĐãNhận, 4, 0, 0, 0) != 4) return 12;
    if (nhậnDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, giáTrịĐãNhận, 4, 0, 0, 0) != -1 || sốLỗi != 11) return 13;
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < 4; chỉSốThứBậc++) if (gửiDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, giáTrịNộiDung, sizeof(giáTrịNộiDung), 0, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến)) != sizeof(giáTrịNộiDung)) return 14;
    if (gửiDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, giáTrịNộiDung, sizeof(giáTrịNộiDung), 0, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến)) != -1 || sốLỗi != 11) return 15;
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < 4; chỉSốThứBậc++) if (nhậnDữLiệuĐiệnDữLiệu(điểmCuốiBộNhận, giáTrịĐãNhận, sizeof(giáTrịĐãNhận), 0, 0, 0) != sizeof(giáTrịNộiDung)) return 16;
    if (gửiDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, 0, 0, 0, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến)) != 0 ||
        nhậnDữLiệuĐiệnDữLiệu(điểmCuốiBộNhận, 0, 0, 0, 0, 0) != 0) return 21;
    giáTrịĐến.ĐịaChỉLiênMạng.giáTrịĐịaChỉ = sốNguyênMạng(0x08080808);
    if (gửiDữLiệuĐiệnDữLiệu(điểmCuốiĐangGửi, giáTrịNộiDung, sizeof(giáTrịNộiDung), 0, (ĐịaChỉỔCắmMạng *)&giáTrịĐến, sizeof(giáTrịĐến)) != -1 || sốLỗi != 101) return 17;
    if (tạoĐiểmCuối(HọLiênMạng, MạngLuồng, GiaoThứcĐiệnDữLiệu) != -1 || sốLỗi != 93) return 18;
    độDàiĐịaChỉ = sizeof(địaChỉĐãGửi);
    if (đọcĐịaChỉỔCắmMạng(điểmCuốiBộNhận, (ĐịaChỉỔCắmMạng *)&địaChỉĐãGửi, &độDàiĐịaChỉ) || ngắnKiểuThứTựThiếtBị(địaChỉĐãGửi.sốCổng) != 7777) return 19;
    if (đóngTệp(điểmCuốiBộNhận) || đóngTệp(điểmCuốiBộNhận) != -1 || sốLỗi != 9) return 20;
    // 보내는곳은 열어 둔다: chươngTrìnhRa 시 프로세스별 socket 정리를 검사한다.
    static const char làĐầyĐủ[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    ghiDữLiệuTệp(1, làĐầyĐủ, sizeof(làĐầyĐủ) - 1);
    return 0;
}
