// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.Nhân;

import Việt_Nam.JVnmOS.VùngNhớ.BộQuảnLýBộNhớ;
import Việt_Nam.JVnmOS.VùngNhớ.BộQuảnLýTrang;
import Việt_Nam.JVnmOS.giáTrịVào.BộQuảnLýĐầuVào;
import Việt_Nam.JVnmOS.TácVụ.giáTrịTiếnTrình;
import Việt_Nam.JVnmOS.TácVụ.BộLậpLịch;
import Việt_Nam.JVnmOS.LờiGọiHệThống.LờiGọiHệThống;
import Việt_Nam.JVnmOS.HệThốngTệp.bảngTraBộMôTảTệp;
import Việt_Nam.JVnmOS.HệThốngTệp.HệThốngTệp;

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
        ThiếtBị.đầuRaNốiTiếp("=== JVnmOS 관리 giáTrịNhân ===\n");
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
