// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.Nhân;

import Hoa_Kỳ.JUsaOS.VùngNhớ.BộQuảnLýBộNhớ;
import Hoa_Kỳ.JUsaOS.VùngNhớ.BộQuảnLýTrang;
import Hoa_Kỳ.JUsaOS.giáTrịVào.BộQuảnLýĐầuVào;
import Hoa_Kỳ.JUsaOS.TácVụ.giáTrịTiếnTrình;
import Hoa_Kỳ.JUsaOS.TácVụ.BộLậpLịch;
import Hoa_Kỳ.JUsaOS.LờiGọiHệThống.LờiGọiHệThống;
import Hoa_Kỳ.JUsaOS.HệThốngTệp.bảngTraBộMôTảTệp;
import Hoa_Kỳ.JUsaOS.HệThốngTệp.HệThốngTệp;

/** Lắp ráp và khởi động nhân do Java quản lý. */
public final class Nhân {
    private final giáTrịPhầnCứng ThiếtBị;
    private final BộQuảnLýBộNhớ VùngNhớ = new BộQuảnLýBộNhớ(32 * 1024 * 1024);
    private final BộQuảnLýTrang quảnTrịTrang = new BộQuảnLýTrang();
    private final HệThốngTệp HệThốngTệp = new HệThốngTệp();
    private final BộLậpLịch BộLậpLịch = new BộLậpLịch(quảnTrịTrang);
    private final BộQuảnLýĐầuVào QuảnTrịĐầuVào = new BộQuảnLýĐầuVào(256);
    private final giáTrịTiếnTrình tiếnTrìnhĐầuTiên;
    private final LờiGọiHệThống LờiGọiHệThống;

    public Nhân(giáTrịPhầnCứng ThiếtBị) {
        this.ThiếtBị = ThiếtBị;
        tiếnTrìnhĐầuTiên = BộLậpLịch.tiếnTrìnhĐầuTiên(new bảngTraBộMôTảTệp(HệThốngTệp));
        LờiGọiHệThống = new LờiGọiHệThống(HệThốngTệp, quảnTrịTrang, BộLậpLịch, ThiếtBị, QuảnTrịĐầuVào);
    }

    public void chạy() {
        ThiếtBị.đầuRaNốiTiếp("=== JUsaOS 관리 giáTrịNhân ===\n");
    }

    public void thựcThiBước() {
        ThiếtBị.cPUDừngHẳn();
    }

    public BộQuảnLýBộNhớ VùngNhớ() {
        return VùngNhớ;
    }

    public BộQuảnLýTrang quảnTrịTrang() {
        return quảnTrịTrang;
    }

    public HệThốngTệp HệThốngTệp() {
        return HệThốngTệp;
    }

    public BộLậpLịch BộLậpLịch() {
        return BộLậpLịch;
    }

    public BộQuảnLýĐầuVào QuảnTrịĐầuVào() {
        return QuảnTrịĐầuVào;
    }

    public giáTrịTiếnTrình tiếnTrìnhĐầuTiên() {
        return tiếnTrìnhĐầuTiên;
    }

    public LờiGọiHệThống LờiGọiHệThống() {
        return LờiGọiHệThống;
    }
}
