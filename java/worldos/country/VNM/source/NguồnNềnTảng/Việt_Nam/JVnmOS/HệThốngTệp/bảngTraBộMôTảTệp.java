// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.HệThốngTệp;

import java.util.HashMap;
import java.util.Map;

/** Giữ bộ mô tả riêng cho từng tiến trình và mô tả tệp đang mở có thể chia sẻ. */
public final class bảngTraBộMôTảTệp {
    private static final int bộMôTảTốiĐa = 32;

    private static final class mụcBộMôTả {
        private final HệThốngTệp.tệpĐãMở tệpĐãMở;
        private boolean đóngThựcThiẢnhBậtTrạngThái;

        mụcBộMôTả(HệThốngTệp.tệpĐãMở tệpĐãMở) {
            this.tệpĐãMở = tệpĐãMở;
        }
    }

    private final HệThốngTệp HệThốngTệp;
    private final Map<Integer, mụcBộMôTả> cácMụcBộMôTả = new HashMap<Integer, mụcBộMôTả>();

    public bảngTraBộMôTảTệp(HệThốngTệp HệThốngTệp) {
        this.HệThốngTệp = HệThốngTệp;
    }

    public int mở(String tên) {
        HệThốngTệp.tệpĐãMở tệpĐãMở = HệThốngTệp.mở(tên);
        if (tệpĐãMở == null) {
            return -2;
        }
        int sốHiệu = chỉSốRỗng(3);
        if (sốHiệu < 0) {
            return -24;
        }
        cácMụcBộMôTả.put(Integer.valueOf(sốHiệu), new mụcBộMôTả(tệpĐãMở));
        return sốHiệu;
    }

    public int đọc(int sốHiệu, byte[] nhậnĐích, int cỡ) {
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return -9;
        }
        if (cỡ < 0 || cỡ > nhậnĐích.length) {
            return -22;
        }
        int dữLiệuSốDư = giáTrịMục.tệpĐãMở.DữLiệu.length - giáTrịMục.tệpĐãMở.vịTrí;
        int đọcCỡ = Math.min(cỡ, Math.max(dữLiệuSốDư, 0));
        System.arraycopy(giáTrịMục.tệpĐãMở.DữLiệu, giáTrịMục.tệpĐãMở.vịTrí, nhậnĐích, 0, đọcCỡ);
        giáTrịMục.tệpĐãMở.vịTrí += đọcCỡ;
        return đọcCỡ;
    }

    public int vịTríDiChuyển(int sốHiệu, int giáTrịKhoảngCách, int gốcCâyDựÁn) {
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return -9;
        }
        int giáTrịNền;
        if (gốcCâyDựÁn == 0) {
            giáTrịNền = 0;
        } else if (gốcCâyDựÁn == 1) {
            giáTrịNền = giáTrịMục.tệpĐãMở.vịTrí;
        } else if (gốcCâyDựÁn == 2) {
            giáTrịNền = giáTrịMục.tệpĐãMở.DữLiệu.length;
        } else {
            return -22;
        }
        int vịTríMới = giáTrịNền + giáTrịKhoảngCách;
        if (vịTríMới < 0) {
            return -22;
        }
        giáTrịMục.tệpĐãMở.vịTrí = vịTríMới;
        return vịTríMới;
    }

    public int đóng(int sốHiệu) {
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.remove(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return -9;
        }
        giáTrịMục.tệpĐãMở.sốLượngThamChiếu--;
        return 0;
    }

    public int bộMôTảĐãNhânBản(int sốHiệu, int sốTốiThiểu) {
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return -9;
        }
        int sốMới = chỉSốRỗng(sốTốiThiểu);
        if (sốMới < 0) {
            return -24;
        }
        giáTrịMục.tệpĐãMở.sốLượngThamChiếu++;
        cácMụcBộMôTả.put(Integer.valueOf(sốMới), new mụcBộMôTả(giáTrịMục.tệpĐãMở));
        return sốMới;
    }

    public int tạiBảnSao(int sốHiệu, int sốMới) {
        if (sốHiệu == sốMới) {
            return cácMụcBộMôTả.containsKey(Integer.valueOf(sốHiệu)) ? sốHiệu : -9;
        }
        if (sốMới < 0 || sốMới >= bộMôTảTốiĐa) {
            return -9;
        }
        mụcBộMôTả nguyênBản = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (nguyênBản == null) {
            return -9;
        }
        if (cácMụcBộMôTả.containsKey(Integer.valueOf(sốMới))) {
            đóng(sốMới);
        }
        nguyênBản.tệpĐãMở.sốLượngThamChiếu++;
        cácMụcBộMôTả.put(Integer.valueOf(sốMới), new mụcBộMôTả(nguyênBản.tệpĐãMở));
        return sốMới;
    }

    public int đặtGiáTrịThựcThiẢnhBậtTrạngTháiĐóng(int sốHiệu, boolean giáTrị) {
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return -9;
        }
        giáTrịMục.đóngThựcThiẢnhBậtTrạngThái = giáTrị;
        return 0;
    }

    public int đóngGiáTrịThựcThiẢnhBậtTrạngThái(int sốHiệu) {
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return -9;
        }
        return giáTrịMục.đóngThựcThiẢnhBậtTrạngThái ? 1 : 0;
    }

    public thôngTinTệp thôngTinHệThống(int sốHiệu) {
        if (sốHiệu >= 0 && sốHiệu <= 2) {
            return new thôngTinTệp(0, 0020666);
        }
        mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(Integer.valueOf(sốHiệu));
        if (giáTrịMục == null) {
            return null;
        }
        return new thôngTinTệp(giáTrịMục.tệpĐãMở.DữLiệu.length, 0100444);
    }

    public void đóngThựcThiẢnhBậtTrạngThái() {
        Integer[] danhSáchSố = cácMụcBộMôTả.keySet().toArray(new Integer[0]);
        for (Integer sốHiệu : danhSáchSố) {
            mụcBộMôTả giáTrịMục = cácMụcBộMôTả.get(sốHiệu);
            if (giáTrịMục != null && giáTrịMục.đóngThựcThiẢnhBậtTrạngThái) {
                đóng(sốHiệu.intValue());
            }
        }
    }

    public boolean làMở(int sốHiệu) {
        return cácMụcBộMôTả.containsKey(Integer.valueOf(sốHiệu));
    }

    public bảngTraBộMôTảTệp giáTrịNhânBản() {
        bảngTraBộMôTảTệp kếtQuả = new bảngTraBộMôTảTệp(HệThốngTệp);
        for (Map.Entry<Integer, mụcBộMôTả> giáTrịMục : cácMụcBộMôTả.entrySet()) {
            giáTrịMục.getValue().tệpĐãMở.sốLượngThamChiếu++;
            mụcBộMôTả bộMôTảMới = new mụcBộMôTả(giáTrịMục.getValue().tệpĐãMở);
            bộMôTảMới.đóngThựcThiẢnhBậtTrạngThái = giáTrịMục.getValue().đóngThựcThiẢnhBậtTrạngThái;
            kếtQuả.cácMụcBộMôTả.put(giáTrịMục.getKey(), bộMôTảMới);
        }
        return kếtQuả;
    }

    private int chỉSốRỗng(int sốTốiThiểu) {
        for (int sốHiệu = Math.max(0, sốTốiThiểu); sốHiệu < bộMôTảTốiĐa; sốHiệu++) {
            if (!cácMụcBộMôTả.containsKey(Integer.valueOf(sốHiệu))) {
                return sốHiệu;
            }
        }
        return -1;
    }
}
