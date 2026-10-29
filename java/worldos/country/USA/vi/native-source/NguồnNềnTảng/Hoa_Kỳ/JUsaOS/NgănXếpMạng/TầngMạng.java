// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.NgănXếpMạng;

import java.util.HashMap;
import java.util.Map;

/** Phân phối tập trung gói nhận Ethernet, ARP, IPv4, ICMP, UDP và TCP. */
public final class TầngMạng {
    @FunctionalInterface
    public interface bộXửLýDữLiệu {
        void mụcGiáTrịTiếnTrình(byte[] DữLiệu, int chạy, int độDài);
    }

    private final Map<Integer, bộXửLýDữLiệu> BộXửLýEthernet = new HashMap<Integer, bộXửLýDữLiệu>();
    private final Map<Integer, bộXửLýDữLiệu> BộXửLýGiaoThứcLiênMạng = new HashMap<Integer, bộXửLýDữLiệu>();
    private final Map<Integer, bộXửLýDữLiệu> bộXửLýĐơnVịDữLiệuNgườiDùng = new HashMap<Integer, bộXửLýDữLiệu>();
    private final Map<Integer, bộXửLýDữLiệu> BộXửLýĐiềuKhiểnSựTruyền = new HashMap<Integer, bộXửLýDữLiệu>();

    public void thanhGhiEthernet(int giáTrịLoại, bộXửLýDữLiệu BộXửLý) {
        BộXửLýEthernet.put(Integer.valueOf(giáTrịLoại & 0xffff), BộXửLý);
    }

    public void thanhGhiGiaoThứcLiênMạng(int giáTrịQuyƯớc, bộXửLýDữLiệu BộXửLý) {
        BộXửLýGiaoThứcLiênMạng.put(Integer.valueOf(giáTrịQuyƯớc & 0xff), BộXửLý);
    }

    public void thanhGhiĐơnVịDữLiệuNgườiDùng(int cổngPhầnCứng, bộXửLýDữLiệu BộXửLý) {
        bộXửLýĐơnVịDữLiệuNgườiDùng.put(Integer.valueOf(cổngPhầnCứng & 0xffff), BộXửLý);
    }

    public void thanhGhiĐiềuKhiểnSựTruyền(int cổngPhầnCứng, bộXửLýDữLiệu BộXửLý) {
        BộXửLýĐiềuKhiểnSựTruyền.put(Integer.valueOf(cổngPhầnCứng & 0xffff), BộXửLý);
    }

    public boolean nhậnEthernet(byte[] chỉSốKhung) {
        if (!CácCôngCụMạng.làKhungEthernet(chỉSốKhung)) {
            return false;
        }
        int giáTrịLoại = CácCôngCụMạng.giaoThứcThượngEthernet(chỉSốKhung);
        bộXửLýDữLiệu BộXửLýTrựcTiếp = BộXửLýEthernet.get(Integer.valueOf(giáTrịLoại));
        if (BộXửLýTrựcTiếp != null) {
            BộXửLýTrựcTiếp.mụcGiáTrịTiếnTrình(chỉSốKhung, 14, chỉSốKhung.length - 14);
            return true;
        }
        return giáTrịLoại == 0x0800 && nhậnGóiTinLiênMạng(chỉSốKhung, 14);
    }

    private boolean nhậnGóiTinLiênMạng(byte[] DữLiệu, int chạy) {
        if (!CácCôngCụMạng.làGiaoThức4PhiênBảnIP(DữLiệu, chạy)) {
            return false;
        }
        int độDàiĐầuMục = (DữLiệu[chạy] & 0x0f) * 4;
        int độDàiTổngCộng = CácCôngCụMạng.ngắnKiểuThứTựByteLớn(DữLiệu, chạy + 2);
        if (độDàiTổngCộng < độDàiĐầuMục || chạy + độDàiTổngCộng > DữLiệu.length) {
            return false;
        }
        int giáTrịQuyƯớc = DữLiệu[chạy + 9] & 0xff;
        int bắtChạyNộiDung = chạy + độDàiĐầuMục;
        int độDàiNộiDung = độDàiTổngCộng - độDàiĐầuMục;
        bộXửLýDữLiệu BộXửLýTrựcTiếp = BộXửLýGiaoThứcLiênMạng.get(Integer.valueOf(giáTrịQuyƯớc));
        if (BộXửLýTrựcTiếp != null) {
            BộXửLýTrựcTiếp.mụcGiáTrịTiếnTrình(DữLiệu, bắtChạyNộiDung, độDàiNộiDung);
            return true;
        }
        if (độDàiNộiDung < 4) {
            return false;
        }
        int sốCổngĐích = CácCôngCụMạng.ngắnKiểuThứTựByteLớn(DữLiệu, bắtChạyNộiDung + 2);
        Map<Integer, bộXửLýDữLiệu> bảngTraCổng = giáTrịQuyƯớc == 17 ? bộXửLýĐơnVịDữLiệuNgườiDùng : giáTrịQuyƯớc == 6 ? BộXửLýĐiềuKhiểnSựTruyền : null;
        if (bảngTraCổng == null) {
            return false;
        }
        bộXửLýDữLiệu bộXửLýCổng = bảngTraCổng.get(Integer.valueOf(sốCổngĐích));
        if (bộXửLýCổng == null) {
            return false;
        }
        bộXửLýCổng.mụcGiáTrịTiếnTrình(DữLiệu, bắtChạyNộiDung, độDàiNộiDung);
        return true;
    }
}

