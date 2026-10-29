// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.VùngNhớ;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** Cung cấp ánh xạ trang 4 KiB và sao chép khi ghi. */
public final class BộQuảnLýTrang {
    public static final int cỡTrang = 4096;

    private static final class giáTrịTrang {
        private byte[] DữLiệu = new byte[cỡTrang];
        private int sốLượngThamChiếu = 1;
        private boolean cóThểGhi = true;
        private boolean saoChépGhiBậtTrạngThái;
    }

    public static final class KhôngGianĐịaChỉ {
        private final Map<Integer, giáTrịTrang> bảngTraTrang = new HashMap<Integer, giáTrịTrang>();
    }

    public KhôngGianĐịaChỉ khôngGianĐịaChỉMới() {
        return new KhôngGianĐịaChỉ();
    }

    public void trangÁnhXạ(KhôngGianĐịaChỉ miềnĐịaChỉ, int địaChỉẢo, boolean cóThểGhi) {
        int sốHiệu = sốTrang(địaChỉẢo);
        giáTrịTrang trangMới = new giáTrịTrang();
        trangMới.cóThểGhi = cóThểGhi;
        miềnĐịaChỉ.bảngTraTrang.put(Integer.valueOf(sốHiệu), trangMới);
    }

    public KhôngGianĐịaChỉ ghiBậtTrạngTháiSaoChépNhânBản(KhôngGianĐịaChỉ nguyênBản) {
        KhôngGianĐịaChỉ giáTrịĐãNhânBản = new KhôngGianĐịaChỉ();
        for (Map.Entry<Integer, giáTrịTrang> giáTrịMục : nguyênBản.bảngTraTrang.entrySet()) {
            giáTrịTrang trangDùngChung = giáTrịMục.getValue();
            trangDùngChung.sốLượngThamChiếu++;
            if (trangDùngChung.cóThểGhi) {
                trangDùngChung.cóThểGhi = false;
                trangDùngChung.saoChépGhiBậtTrạngThái = true;
            }
            giáTrịĐãNhânBản.bảngTraTrang.put(giáTrịMục.getKey(), trangDùngChung);
        }
        return giáTrịĐãNhânBản;
    }

    public byte đọcGiáTrịByte(KhôngGianĐịaChỉ miềnĐịaChỉ, int địaChỉẢo) {
        giáTrịTrang giáTrịĐốiĐích = tìmTrang(miềnĐịaChỉ, địaChỉẢo);
        return giáTrịĐốiĐích.DữLiệu[Math.floorMod(địaChỉẢo, cỡTrang)];
    }

    public void ghiGiáTrịByte(KhôngGianĐịaChỉ miềnĐịaChỉ, int địaChỉẢo, byte giáTrị) {
        int sốHiệu = sốTrang(địaChỉẢo);
        giáTrịTrang giáTrịĐốiĐích = tìmTrang(miềnĐịaChỉ, địaChỉẢo);
        if (!giáTrịĐốiĐích.cóThểGhi) {
            if (!giáTrịĐốiĐích.saoChépGhiBậtTrạngThái) {
                throw new IllegalStateException("đọc 전용 쪽입니다.");
            }
            giáTrịĐốiĐích = tạoTrangRiêngTư(miềnĐịaChỉ, sốHiệu, giáTrịĐốiĐích);
        }
        giáTrịĐốiĐích.DữLiệu[Math.floorMod(địaChỉẢo, cỡTrang)] = giáTrị;
    }

    public void ghiKhoảngRiêngTư(KhôngGianĐịaChỉ miềnĐịaChỉ, int bắtChạyĐịaChỉ, int cỡ) {
        if (cỡ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int địaChỉKếtThúc = Math.addExact(bắtChạyĐịaChỉ, cỡ);
        for (int địaChỉ = bắtChạyĐịaChỉ; địaChỉ < địaChỉKếtThúc; địaChỉ = (sốTrang(địaChỉ) + 1) * cỡTrang) {
            int sốHiệu = sốTrang(địaChỉ);
            giáTrịTrang giáTrịĐốiĐích = tìmTrang(miềnĐịaChỉ, địaChỉ);
            if (giáTrịĐốiĐích.saoChépGhiBậtTrạngThái) {
                tạoTrangRiêngTư(miềnĐịaChỉ, sốHiệu, giáTrịĐốiĐích);
            } else {
                giáTrịĐốiĐích.cóThểGhi = true;
            }
        }
    }

    public void ghiKhoảng(KhôngGianĐịaChỉ miềnĐịaChỉ, int bắtChạyĐịaChỉ, byte[] DữLiệu) {
        for (int sốHiệu = 0; sốHiệu < DữLiệu.length; sốHiệu++) {
            ghiGiáTrịByte(miềnĐịaChỉ, bắtChạyĐịaChỉ + sốHiệu, DữLiệu[sốHiệu]);
        }
    }

    private giáTrịTrang tạoTrangRiêngTư(KhôngGianĐịaChỉ miềnĐịaChỉ, int sốHiệu, giáTrịTrang trangDùngChung) {
        giáTrịTrang trangRiêngTư = new giáTrịTrang();
        trangRiêngTư.DữLiệu = Arrays.copyOf(trangDùngChung.DữLiệu, trangDùngChung.DữLiệu.length);
        trangRiêngTư.cóThểGhi = true;
        trangRiêngTư.saoChépGhiBậtTrạngThái = false;
        trangDùngChung.sốLượngThamChiếu--;
        miềnĐịaChỉ.bảngTraTrang.put(Integer.valueOf(sốHiệu), trangRiêngTư);
        return trangRiêngTư;
    }

    private giáTrịTrang tìmTrang(KhôngGianĐịaChỉ miềnĐịaChỉ, int địaChỉ) {
        giáTrịTrang giáTrịĐốiĐích = miềnĐịaChỉ.bảngTraTrang.get(Integer.valueOf(sốTrang(địaChỉ)));
        if (giáTrịĐốiĐích == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return giáTrịĐốiĐích;
    }

    private int sốTrang(int địaChỉ) {
        if (địaChỉ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return địaChỉ / cỡTrang;
    }
}

