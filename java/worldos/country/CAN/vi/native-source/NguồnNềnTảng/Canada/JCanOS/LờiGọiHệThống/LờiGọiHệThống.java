// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.LờiGọiHệThống;

import Canada.JCanOS.VùngNhớ.BộQuảnLýTrang;
import Canada.JCanOS.TácVụ.giáTrịTiếnTrình;
import Canada.JCanOS.TácVụ.BộLậpLịch;
import Canada.JCanOS.HệThốngTệp.BộNạpTệpThựcThi;
import Canada.JCanOS.HệThốngTệp.HệThốngTệp;
import Canada.JCanOS.HệThốngTệp.thôngTinTệp;
import Canada.JCanOS.Nhân.giáTrịPhầnCứng;
import Canada.JCanOS.giáTrịVào.BộQuảnLýĐầuVào;
import Canada.JCanOS.giáTrịVào.sựKiệnĐầuVào;

/** Lớp Java quản lý lời gọi POSIX giai đoạn một của engos. */
public final class LờiGọiHệThống {
    public static final int đọcCờChỉ = 0;
    public static final int tìmKiếmBắtChạy = 0;
    public static final int tìmKiếmHiệnTại = 1;
    public static final int tìmKếtThúcMục = 2;

    private final HệThốngTệp HệThốngTệp;
    private final BộQuảnLýTrang quảnTrịTrang;
    private final BộLậpLịch BộLậpLịch;
    private final BộNạpTệpThựcThi bộNạp = new BộNạpTệpThựcThi();
    private final giáTrịPhầnCứng ThiếtBị;
    private final BộQuảnLýĐầuVào QuảnTrịĐầuVào;

    public LờiGọiHệThống(HệThốngTệp HệThốngTệp, BộQuảnLýTrang quảnTrịTrang, BộLậpLịch BộLậpLịch, giáTrịPhầnCứng ThiếtBị, BộQuảnLýĐầuVào QuảnTrịĐầuVào) {
        this.HệThốngTệp = HệThốngTệp;
        this.quảnTrịTrang = quảnTrịTrang;
        this.BộLậpLịch = BộLậpLịch;
        this.ThiếtBị = ThiếtBị;
        this.QuảnTrịĐầuVào = QuảnTrịĐầuVào;
    }

    public int địnhDanhTiếnTrình(giáTrịTiếnTrình tiếnTrìnhHiệnTại) {
        return tiếnTrìnhHiệnTại.giáTrịĐịnhDanh();
    }

    public int địnhDanhTiếnTrìnhCha(giáTrịTiếnTrình tiếnTrìnhHiệnTại) {
        return tiếnTrìnhHiệnTại.địnhDanhCha();
    }

    public int mở(giáTrịTiếnTrình tiếnTrìnhHiệnTại, String tên, int giáTrịCờ) {
        if (giáTrịCờ != đọcCờChỉ) {
            return -30;
        }
        return tiếnTrìnhHiệnTại.bộMôTảTệp().mở(tên);
    }

    public int đọc(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả, byte[] nhậnĐích, int cỡ) {
        if (mụcBộMôTả == 0) {
            if (cỡ <= 0 || nhậnĐích.length == 0) {
                return 0;
            }
            sựKiệnĐầuVào sựKiện = QuảnTrịĐầuVào.sựKiệnKếTiếp();
            if (sựKiện == null || sựKiện.loạiSựKiện() != sựKiệnĐầuVào.giáTrịLoại.xuốngPhím) {
                return -11;
            }
            nhậnĐích[0] = (byte) sựKiện.giáTrịĐầuTiên();
            return 1;
        }
        return tiếnTrìnhHiệnTại.bộMôTảTệp().đọc(mụcBộMôTả, nhậnĐích, cỡ);
    }

    public int ghi(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả, byte[] DữLiệu, int cỡ) {
        if (mụcBộMôTả != 1 && mụcBộMôTả != 2) {
            return tiếnTrìnhHiệnTại.bộMôTảTệp().làMở(mụcBộMôTả) ? -30 : -9;
        }
        if (cỡ < 0 || cỡ > DữLiệu.length) {
            return -22;
        }
        ThiếtBị.đầuRaNốiTiếp(new String(DữLiệu, 0, cỡ, java.nio.charset.StandardCharsets.UTF_8));
        return cỡ;
    }

    public int đóng(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả) {
        return tiếnTrìnhHiệnTại.bộMôTảTệp().đóng(mụcBộMôTả);
    }

    public int vịTríDiChuyển(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả, int giáTrịKhoảngCách, int gốcCâyDựÁn) {
        return tiếnTrìnhHiệnTại.bộMôTảTệp().vịTríDiChuyển(mụcBộMôTả, giáTrịKhoảngCách, gốcCâyDựÁn);
    }

    public int bộMôTảBảnSao(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả) {
        return tiếnTrìnhHiệnTại.bộMôTảTệp().bộMôTảĐãNhânBản(mụcBộMôTả, 0);
    }

    public int tạiBộMôTảBảnSao(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả, int bộMôTảMới) {
        return tiếnTrìnhHiệnTại.bộMôTảTệp().tạiBảnSao(mụcBộMôTả, bộMôTảMới);
    }

    public int làTruyCậpĐược(String tên, int chếĐộPhươngThức) {
        thôngTinTệp thôngTinHệThống = HệThốngTệp.thôngTinHệThống(tên);
        if (thôngTinHệThống == null) {
            return -2;
        }
        if ((chếĐộPhươngThức & 1) != 0 && (thôngTinHệThống.loạiHình() & 0111) == 0) {
            return -13;
        }
        if ((chếĐộPhươngThức & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int danhSáchTácVụChuyển(String tên) {
        return "/".equals(tên) ? 0 : -20;
    }

    public String danhSáchTácVụHiệnTại(int nhậnCỡ) {
        return nhậnCỡ >= 2 ? "/" : null;
    }

    public int địnhDanhNgườiDùng() { return 0; }
    public int địnhDanhNgườiDùngHiệuLực() { return 0; }
    public int địnhDanhNhóm() { return 0; }
    public int địnhDanhNhómHiệuLực() { return 0; }

    public int đồngBộHóaTệp(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả) {
        return tiếnTrìnhHiệnTại.bộMôTảTệp().thôngTinHệThống(mụcBộMôTả) == null ? -9 : 0;
    }

    public void đồngBộHóaTấtCả() {
        // Hệ thống tệp hiện tại chỉ đọc nên không có dữ liệu cần đẩy ra.
    }

    public boolean làThiếtBịCuối(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả) {
        thôngTinTệp thôngTinHệThống = tiếnTrìnhHiệnTại.bộMôTảTệp().thôngTinHệThống(mụcBộMôTả);
        return thôngTinHệThống != null && (thôngTinHệThống.loạiHình() & 0170000) == 0020000;
    }

    public int điềuKhiểnTệp(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả, int lệnh, int đốiSốThamSố) {
        if (lệnh == 0) {
            return tiếnTrìnhHiệnTại.bộMôTảTệp().bộMôTảĐãNhânBản(mụcBộMôTả, đốiSốThamSố);
        }
        if (lệnh == 1) {
            return tiếnTrìnhHiệnTại.bộMôTảTệp().đóngGiáTrịThựcThiẢnhBậtTrạngThái(mụcBộMôTả);
        }
        if (lệnh == 2) {
            return tiếnTrìnhHiệnTại.bộMôTảTệp().đặtGiáTrịThựcThiẢnhBậtTrạngTháiĐóng(mụcBộMôTả, (đốiSốThamSố & 1) != 0);
        }
        if (lệnh == 3) {
            return tiếnTrìnhHiệnTại.bộMôTảTệp().thôngTinHệThống(mụcBộMôTả) == null ? -9 : đọcCờChỉ;
        }
        if (lệnh == 4) {
            return đốiSốThamSố == đọcCờChỉ ? 0 : -30;
        }
        return -22;
    }

    public int tạoMục(String tên, int giáTrịQuyền) {
        return -30;
    }

    public thôngTinTệp thôngTinBộMôTả(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int mụcBộMôTả) {
        return tiếnTrìnhHiệnTại.bộMôTảTệp().thôngTinHệThống(mụcBộMôTả);
    }

    public cácChiTiếtHệThống cácChiTiếtHệThống() {
        return new cácChiTiếtHệThống("JCanOS", "JCanOS", "0.1", "Java managed kernel", "i386");
    }

    public thôngTinTệp thôngTinTệp(String tên) {
        return HệThốngTệp.thôngTinHệThống(tên);
    }

    public giáTrịTiếnTrình tiếnTrìnhNhânBản(giáTrịTiếnTrình giáTrịCha) {
        return BộLậpLịch.giáTrịNhânBản(giáTrịCha);
    }

    public int chờConCho(giáTrịTiếnTrình giáTrịCha, int địnhDanhCon, boolean chặnPhi) {
        return BộLậpLịch.chờConCho(giáTrịCha, địnhDanhCon, chặnPhi);
    }

    public int ngắtChươngTrình(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int kếtThúcMới) {
        int kếtThúcTrướcĐó = tiếnTrìnhHiệnTại.ngắtChươngTrình();
        if (kếtThúcMới == 0) {
            return kếtThúcTrướcĐó;
        }
        if (kếtThúcMới < 0x06000000 || kếtThúcMới > 0x07000000) {
            return -12;
        }
        int trangĐầuTiên = kếtThúcTrướcĐó / BộQuảnLýTrang.cỡTrang;
        int trangCuối = (kếtThúcMới + BộQuảnLýTrang.cỡTrang - 1) / BộQuảnLýTrang.cỡTrang;
        if (kếtThúcMới > kếtThúcTrướcĐó) {
            for (int sốHiệu = trangĐầuTiên; sốHiệu < trangCuối; sốHiệu++) {
                int địaChỉ = sốHiệu * BộQuảnLýTrang.cỡTrang;
                try {
                    quảnTrịTrang.đọcGiáTrịByte(tiếnTrìnhHiệnTại.KhôngGianĐịaChỉ(), địaChỉ);
                } catch (IllegalStateException lỗi) {
                    quảnTrịTrang.trangÁnhXạ(tiếnTrìnhHiệnTại.KhôngGianĐịaChỉ(), địaChỉ, true);
                }
            }
        }
        tiếnTrìnhHiệnTại.đặtGiáTrịNgắtChươngTrình(kếtThúcMới);
        return kếtThúcMới;
    }

    public int tăngNgắtChươngTrình(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int lượngBướcTăng) {
        int kếtThúcTrướcĐó = tiếnTrìnhHiệnTại.ngắtChươngTrình();
        int kếtQuả = ngắtChươngTrình(tiếnTrìnhHiệnTại, kếtThúcTrướcĐó + lượngBướcTăng);
        return kếtQuả < 0 ? kếtQuả : kếtThúcTrướcĐó;
    }

    public int thựcThiLệnh(giáTrịTiếnTrình tiếnTrìnhHiệnTại, byte[] tệpTệpThựcThi) {
        return thựcThiLệnh(tiếnTrìnhHiệnTại, tệpTệpThựcThi, new String[0], new String[0]);
    }

    public int thựcThiLệnh(giáTrịTiếnTrình tiếnTrìnhHiệnTại, byte[] tệpTệpThựcThi, String[] đốiSốThamSố, String[] môiTrường) {
        BộNạpTệpThựcThi.ảnh giáTrịẢnh;
        try {
            giáTrịẢnh = bộNạp.CácPhépKiểmTra(tệpTệpThựcThi);
        } catch (IllegalArgumentException lỗi) {
            return -8;
        }
        if (đốiSốThamSố == null || môiTrường == null || đốiSốThamSố.length > 16 || môiTrường.length > 16) {
            return -7;
        }
        for (BộNạpTệpThựcThi.giáTrịMụcĐoạn giáTrịMụcĐoạn : giáTrịẢnh.danhSáchCácMụcĐoạn()) {
            if ((giáTrịMụcĐoạn.giáTrịCờ() & 2) == 0 || giáTrịMụcĐoạn.cỡ() == 0) {
                continue;
            }
            int trangĐầuTiên = giáTrịMụcĐoạn.địaChỉ() / BộQuảnLýTrang.cỡTrang;
            int trangCuối = (giáTrịMụcĐoạn.địaChỉ() + giáTrịMụcĐoạn.cỡ() + BộQuảnLýTrang.cỡTrang - 1) / BộQuảnLýTrang.cỡTrang;
            for (int sốHiệu = trangĐầuTiên; sốHiệu < trangCuối; sốHiệu++) {
                int địaChỉ = sốHiệu * BộQuảnLýTrang.cỡTrang;
                try {
                    quảnTrịTrang.đọcGiáTrịByte(tiếnTrìnhHiệnTại.KhôngGianĐịaChỉ(), địaChỉ);
                    quảnTrịTrang.ghiKhoảngRiêngTư(tiếnTrìnhHiệnTại.KhôngGianĐịaChỉ(), địaChỉ, BộQuảnLýTrang.cỡTrang);
                } catch (IllegalStateException lỗi) {
                    quảnTrịTrang.trangÁnhXạ(tiếnTrìnhHiệnTại.KhôngGianĐịaChỉ(), địaChỉ, true);
                }
            }
            for (int sốHiệu = 0; sốHiệu < giáTrịMụcĐoạn.cỡ(); sốHiệu++) {
                byte giáTrị = giáTrịMụcĐoạn.giáTrịLoại() == 8 ? 0 : tệpTệpThựcThi[giáTrịMụcĐoạn.vịTríTệp() + sốHiệu];
                quảnTrịTrang.ghiGiáTrịByte(tiếnTrìnhHiệnTại.KhôngGianĐịaChỉ(), giáTrịMụcĐoạn.địaChỉ() + sốHiệu, giáTrị);
            }
        }
        tiếnTrìnhHiệnTại.đặtGiáTrịNgữCảnhViệcThựcThi(giáTrịẢnh.bắtChạyĐịaChỉ(), đốiSốThamSố, môiTrường);
        tiếnTrìnhHiệnTại.bộMôTảTệp().đóngThựcThiẢnhBậtTrạngThái();
        return 0;
    }

    public void chươngTrìnhThoátHẳn(giáTrịTiếnTrình tiếnTrìnhHiệnTại, int giáTrịTrạngThái) {
        tiếnTrìnhHiệnTại.chươngTrìnhRa(giáTrịTrạngThái);
    }
}
