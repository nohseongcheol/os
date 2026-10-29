// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.thiếtBịLưuTrữ;

import java.util.Arrays;

/** Thiết bị cung logic 512 byte tương ứng lớp lệnh ATA 28 bit. */
public final class PhầnGắnCôngNghệNângCao {
    public static final int cỡMụcĐoạn = 512;
    private final byte[] DữLiệu;
    private final boolean đọcGiáTrịChỉ;

    public PhầnGắnCôngNghệNângCao(int sốLượngMụcĐoạn, boolean đọcGiáTrịChỉ) {
        if (sốLượngMụcĐoạn <= 0) {
            throw new IllegalArgumentException("giáTrịMụcĐoạn 수가 올바르지 않습니다.");
        }
        DữLiệu = new byte[Math.multiplyExact(sốLượngMụcĐoạn, cỡMụcĐoạn)];
        this.đọcGiáTrịChỉ = đọcGiáTrịChỉ;
    }

    public int sốLượngMụcĐoạn() {
        return DữLiệu.length / cỡMụcĐoạn;
    }

    public void đọc(int chỉSốMụcĐoạn, byte[] nhậnĐích) {
        kiểmTraKhoảng(chỉSốMụcĐoạn, nhậnĐích);
        System.arraycopy(DữLiệu, chỉSốMụcĐoạn * cỡMụcĐoạn, nhậnĐích, 0, cỡMụcĐoạn);
    }

    public void ghi(int chỉSốMụcĐoạn, byte[] ghiĐếnDữLiệu) {
        if (đọcGiáTrịChỉ) {
            throw new IllegalStateException("đọc 전용 장치입니다.");
        }
        kiểmTraKhoảng(chỉSốMụcĐoạn, ghiĐếnDữLiệu);
        System.arraycopy(ghiĐếnDữLiệu, 0, DữLiệu, chỉSốMụcĐoạn * cỡMụcĐoạn, cỡMụcĐoạn);
    }

    public void xóaMục() {
        if (đọcGiáTrịChỉ) {
            throw new IllegalStateException("đọc 전용 장치입니다.");
        }
        Arrays.fill(DữLiệu, (byte) 0);
    }

    private void kiểmTraKhoảng(int chỉSốMụcĐoạn, byte[] khôngGianTạm) {
        if (chỉSốMụcĐoạn < 0 || chỉSốMụcĐoạn >= sốLượngMụcĐoạn() || khôngGianTạm.length < cỡMụcĐoạn) {
            throw new IllegalArgumentException("ATA giáTrịMụcĐoạn 범위가 올바르지 않습니다.");
        }
    }
}

