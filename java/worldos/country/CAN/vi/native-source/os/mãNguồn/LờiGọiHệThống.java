// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Được gọi qua cổng int 0x80. Kiểm tra mọi con trỏ và độ dài của người dùng trước khi truy cập. */
public final class LờiGọiHệThống {
    static int[] bộĐệmTạm = new int[1024];

    static int độDàiMảng(int địaChỉ) {
        if (!QuảnLýThựcThi.cắtXén(địaChỉ, 4)) return -14;
        int độDài = QuảnLýThựcThi.trịSố(địaChỉ);
        if (độDài < 0 || độDài > (QuảnLýThựcThi.kếtThúcNgườiDùng - địaChỉ - 4) / 4) return -14;
        return độDài;
    }

    public static int mụcGiáTrịTiếnTrình(int sốHiệu, int toánHạngĐầuTiên, int toánHạngThứHai, int toánHạngThứBa, int toánHạngThứTư, int toánHạngThứNăm) {
        if (sốHiệu == 30) return QuảnLýMôTảTệp.mởTệp(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 31) return QuảnLýMôTảTệp.đọcTệp(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 32) return QuảnLýMôTảTệp.ghiTệp(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 33) return QuảnLýMôTảTệp.đóngTệp(toánHạngĐầuTiên);
        if (sốHiệu == 34) return QuảnLýMôTảTệp.dịchVịTệp(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 35) return QuảnLýMôTảTệp.bộMôTảBảnSao(toánHạngĐầuTiên, 0, false, 0);
        if (sốHiệu == 36) return QuảnLýMôTảTệp.bộMôTảBảnSao(toánHạngĐầuTiên, toánHạngThứHai, true, 0);
        if (sốHiệu == 37) return QuảnLýMôTảTệp.đọcTìnhTrạngTệp(toánHạngĐầuTiên, toánHạngThứHai);
        if (sốHiệu == 38) return QuảnLýMôTảTệp.gỡTênMụcTệp(toánHạngĐầuTiên);
        if (sốHiệu == 39) return QuảnLýMôTảTệp.đặtGiáTrịĐộDàiTệp(toánHạngĐầuTiên, toánHạngThứHai);
        if (sốHiệu == 40) return QuảnLýMôTảTệp.bộMôTảĐiềuKhiển(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 41) return QuảnLýMôTảTệp.tạoĐiểmCuối(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 42) return QuảnLýMôTảTệp.ràngBuộcĐịaChỉ(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 43) return QuảnLýMôTảTệp.gửiDữLiệuĐiệnDữLiệu(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa, toánHạngThứTư, toánHạngThứNăm);
        if (sốHiệu == 44) return QuảnLýMôTảTệp.nhậnDữLiệuĐiệnDữLiệu(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa, toánHạngThứTư, toánHạngThứNăm);
        if (sốHiệu == 45) return QuảnLýMôTảTệp.đọcĐịaChỉỔCắmMạng(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa);
        if (sốHiệu == 46) return QuảnLýMôTảTệp.đặtGiáTrịHếtGiờNhận(toánHạngĐầuTiên, toánHạngThứHai);
        if (sốHiệu == 47) {
            int giáTrịBộMôTả = QuảnLýMôTảTệp.tìmBộMôTả(toánHạngĐầuTiên);
            if (giáTrịBộMôTả < 0) return -9;
            if (QuảnLýMôTảTệp.giáTrịLoại[giáTrịBộMôTả] != 2) return -22;
            return LưuGiữTệp.đồngBộHóa();
        }
        if (sốHiệu == 1) {
            int độDài = độDàiMảng(toánHạngĐầuTiên);
            if (độDài < 0) return độDài;
            if (độDài > 4096) return -90;
            for (int giáTrịKýTự = 0; giáTrịKýTự < độDài; giáTrịKýTự++) ĐầuCuốiVănBản.KýTự(QuảnLýThựcThi.trịSố(toánHạngĐầuTiên + 4 + giáTrịKýTự * 4) & 65535);
            return độDài;
        }
        if (sốHiệu == 2) return QuảnLýThựcThi.sốLượngĐốiSố;
        if (sốHiệu == 3) return toánHạngĐầuTiên >= 0 && toánHạngĐầuTiên < QuảnLýThựcThi.sốLượngĐốiSố ? QuảnLýThựcThi.địaChỉĐốiSố[toánHạngĐầuTiên] : 0;
        if (sốHiệu == 10) return NgănXếpMạng.mở(toánHạngĐầuTiên);
        if (sốHiệu == 11) {
            int độDài = độDàiMảng(toánHạngThứTư);
            if (độDài < 0) return độDài;
            if (toánHạngThứNăm < 0 || toánHạngThứNăm > độDài || toánHạngThứNăm > 1024) return -90;
            for (int vịTrí = 0; vịTrí < toánHạngThứNăm; vịTrí++) bộĐệmTạm[vịTrí] = QuảnLýThựcThi.trịSố(toánHạngThứTư + 4 + vịTrí * 4) & 255;
            return NgănXếpMạng.gửi(toánHạngĐầuTiên, toánHạngThứHai, toánHạngThứBa, bộĐệmTạm, toánHạngThứNăm);
        }
        if (sốHiệu == 12) {
            int độDài = độDàiMảng(toánHạngThứHai);
            if (độDài < 0) return độDài;
            if (toánHạngThứBa < 0 || toánHạngThứBa > 2000) return -22;
            int kếtQuả = NgănXếpMạng.nhận(toánHạngĐầuTiên, bộĐệmTạm, độDài < 1024 ? độDài : 1024, toánHạngThứBa);
            if (kếtQuả >= 0) for (int vịTrí = 0; vịTrí < kếtQuả; vịTrí++) QuảnLýThựcThi.ghiSố(toánHạngThứHai + 4 + vịTrí * 4, bộĐệmTạm[vịTrí]);
            return kếtQuả;
        }
        if (sốHiệu == 13) return NgănXếpMạng.đóng(toánHạngĐầuTiên);
        if (sốHiệu == 14) return NgănXếpMạng.địaChỉTựCó;
        if (sốHiệu == 15) return NgănXếpMạng.địaChỉĐốiTác(toánHạngĐầuTiên);
        if (sốHiệu == 16) return NgănXếpMạng.sốCổngĐốiTác(toánHạngĐầuTiên);
        if (sốHiệu == 22) {
            if (toánHạngĐầuTiên < 0 || toánHạngĐầuTiên > 65535) return -22;
            ĐầuCuốiVănBản.KýTự(toánHạngĐầuTiên); return 1;
        }
        if (sốHiệu == 20 || sốHiệu == 21) {
            int cỡTên = độDàiMảng(toánHạngĐầuTiên), cỡDữLiệu = độDàiMảng(toánHạngThứHai);
            if (cỡTên < 0 || cỡDữLiệu < 0) return -14;
            if (cỡTên < 1 || cỡTên > 64) return -22;
            int độDài = 0;
            while (độDài < cỡTên && QuảnLýThựcThi.trịSố(toánHạngĐầuTiên + 4 + độDài * 4) != 0) {
                HệTệpBộNhớ.tên[độDài] = QuảnLýThựcThi.trịSố(toánHạngĐầuTiên + 4 + độDài * 4);
                độDài++;
            }
            if (!HệTệpBộNhớ.kiểmTraTên(HệTệpBộNhớ.tên, độDài)) return -22;
            if (sốHiệu == 20) {
                int Tệp = HệTệpBộNhớ.tìmMục(HệTệpBộNhớ.tên, độDài);
                if (Tệp < 0) return Tệp;
                int cỡ = HệTệpBộNhớ.danhSáchCỡ[Tệp];
                if (cỡ > cỡDữLiệu) return -90;
                int địaChỉ = ThiếtBị.bộNhớTệp() + Tệp * HệTệpBộNhớ.cỡTốiĐa;
                for (int trịSố = 0; trịSố < cỡ; trịSố++) QuảnLýThựcThi.ghiSố(toánHạngThứHai + 4 + trịSố * 4, ThiếtBị.đọcBộNhớ(địaChỉ + trịSố));
                return cỡ;
            }
            if (toánHạngThứBa < 0 || toánHạngThứBa > cỡDữLiệu) return -22;
            if (toánHạngThứBa > HệTệpBộNhớ.cỡTốiĐa) return -90;
            for (int trịSố = 0; trịSố < toánHạngThứBa; trịSố++) HệTệpBộNhớ.giáTrịSửa[trịSố] = QuảnLýThựcThi.trịSố(toánHạngThứHai + 4 + trịSố * 4) & 255;
            return HệTệpBộNhớ.giáTrịCất(HệTệpBộNhớ.tên, độDài, HệTệpBộNhớ.giáTrịSửa, toánHạngThứBa);
        }
        return -38;
    }
}
