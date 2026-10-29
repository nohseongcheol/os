// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Trung_Quốc.JChnOS.TácVụ;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Trung_Quốc.JChnOS.VùngNhớ.BộQuảnLýTrang;
import Trung_Quốc.JChnOS.HệThốngTệp.bảngTraBộMôTảTệp;

/** Quản lý mã định danh tiến trình và hàng đợi sẵn sàng luân phiên. */
public final class BộLậpLịch {
    private final BộQuảnLýTrang quảnTrịTrang;
    private final Map<Integer, giáTrịTiếnTrình> danhSáchTiếnTrình = new HashMap<Integer, giáTrịTiếnTrình>();
    private final Queue<giáTrịTiếnTrình> hàngĐợiSẵnSàng = new ArrayDeque<giáTrịTiếnTrình>();
    private int địnhDanhKếTiếp = 1;

    public BộLậpLịch(BộQuảnLýTrang quảnTrịTrang) {
        this.quảnTrịTrang = quảnTrịTrang;
    }

    public giáTrịTiếnTrình tiếnTrìnhĐầuTiên(bảngTraBộMôTảTệp bộMôTảTệp) {
        giáTrịTiếnTrình tiếnTrìnhMới = new giáTrịTiếnTrình(cấpPhátĐịnhDanh(), 0, quảnTrịTrang.khôngGianĐịaChỉMới(), bộMôTảTệp);
        danhSáchTiếnTrình.put(Integer.valueOf(tiếnTrìnhMới.giáTrịĐịnhDanh()), tiếnTrìnhMới);
        hàngĐợiSẵnSàng.offer(tiếnTrìnhMới);
        return tiếnTrìnhMới;
    }

    public giáTrịTiếnTrình giáTrịNhânBản(giáTrịTiếnTrình giáTrịCha) {
        giáTrịTiếnTrình giáTrịCon = new giáTrịTiếnTrình(
                cấpPhátĐịnhDanh(),
                giáTrịCha.giáTrịĐịnhDanh(),
                quảnTrịTrang.ghiBậtTrạngTháiSaoChépNhânBản(giáTrịCha.KhôngGianĐịaChỉ()),
                giáTrịCha.bộMôTảTệp().giáTrịNhânBản());
        giáTrịCon.đặtGiáTrịNgắtChươngTrình(giáTrịCha.ngắtChươngTrình());
        danhSáchTiếnTrình.put(Integer.valueOf(giáTrịCon.giáTrịĐịnhDanh()), giáTrịCon);
        hàngĐợiSẵnSàng.offer(giáTrịCon);
        return giáTrịCon;
    }

    public giáTrịTiếnTrình tiếnTrìnhKếTiếp() {
        int kiểmTraSốLượng = hàngĐợiSẵnSàng.size();
        for (int sốHiệu = 0; sốHiệu < kiểmTraSốLượng; sốHiệu++) {
            giáTrịTiếnTrình phầnMụcKếTiếp = hàngĐợiSẵnSàng.poll();
            if (phầnMụcKếTiếp != null && (phầnMụcKếTiếp.giáTrịTrạngThái() == trạngTháiTiếnTrình.chuẩnBị || phầnMụcKếTiếp.giáTrịTrạngThái() == trạngTháiTiếnTrình.thựcThiLệnh)) {
                phầnMụcKếTiếp.đặtGiáTrịTrạngThái(trạngTháiTiếnTrình.thựcThiLệnh);
                hàngĐợiSẵnSàng.offer(phầnMụcKếTiếp);
                return phầnMụcKếTiếp;
            }
        }
        return null;
    }

    public int chờConCho(giáTrịTiếnTrình giáTrịCha, int địnhDanhCon, boolean chặnPhi) {
        for (giáTrịTiếnTrình ứngViên : danhSáchTiếnTrình.values()) {
            if (ứngViên.địnhDanhCha() != giáTrịCha.giáTrịĐịnhDanh()) {
                continue;
            }
            if (địnhDanhCon > 0 && ứngViên.giáTrịĐịnhDanh() != địnhDanhCon) {
                continue;
            }
            if (ứngViên.giáTrịTrạngThái() == trạngTháiTiếnTrình.chươngTrìnhRa) {
                int kếtQuả = (ứngViên.mãRa() & 0xff) << 8;
                danhSáchTiếnTrình.remove(Integer.valueOf(ứngViên.giáTrịĐịnhDanh()));
                return kếtQuả;
            }
            return chặnPhi ? 0 : -11;
        }
        return -10;
    }

    public giáTrịTiếnTrình tìmTiếnTrình(int giáTrịĐịnhDanh) {
        return danhSáchTiếnTrình.get(Integer.valueOf(giáTrịĐịnhDanh));
    }

    private int cấpPhátĐịnhDanh() {
        return địnhDanhKếTiếp++;
    }
}
