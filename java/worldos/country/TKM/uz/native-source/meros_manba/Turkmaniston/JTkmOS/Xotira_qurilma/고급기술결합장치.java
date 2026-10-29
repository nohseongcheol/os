// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.Xotira_qurilma;

import java.util.Arrays;

/** ATA 28비트 Buyruq 계층과 같은 512바이트 논리 bo_lim_VALUE_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int bo_lim_o_lcham = 512;
    private final byte[] ma_lumotlar;
    private final boolean faqat_o_qish_uchun_VALUE;

    public 고급기술결합장치(int bo_lim_COUNT, boolean faqat_o_qish_uchun_VALUE) {
        if (bo_lim_COUNT <= 0) {
            throw new IllegalArgumentException("bo_lim_VALUE_366e0bfa 수가 올바르지 않습니다.");
        }
        ma_lumotlar = new byte[Math.multiplyExact(bo_lim_COUNT, bo_lim_o_lcham)];
        this.faqat_o_qish_uchun_VALUE = faqat_o_qish_uchun_VALUE;
    }

    public int bo_lim_COUNT() {
        return ma_lumotlar.length / bo_lim_o_lcham;
    }

    public void Oʻqish(int bo_lim_INDEX, byte[] 받을곳) {
        범위확인(bo_lim_INDEX, 받을곳);
        System.arraycopy(ma_lumotlar, bo_lim_INDEX * bo_lim_o_lcham, 받을곳, 0, bo_lim_o_lcham);
    }

    public void Yozish(int bo_lim_INDEX, byte[] 쓸자료) {
        if (faqat_o_qish_uchun_VALUE) {
            throw new IllegalStateException("Oʻqish 전용 장치입니다.");
        }
        범위확인(bo_lim_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, ma_lumotlar, bo_lim_INDEX * bo_lim_o_lcham, bo_lim_o_lcham);
    }

    public void tozalash_kiritish() {
        if (faqat_o_qish_uchun_VALUE) {
            throw new IllegalStateException("Oʻqish 전용 장치입니다.");
        }
        Arrays.fill(ma_lumotlar, (byte) 0);
    }

    private void 범위확인(int bo_lim_INDEX, byte[] 임시공간) {
        if (bo_lim_INDEX < 0 || bo_lim_INDEX >= bo_lim_COUNT() || 임시공간.length < bo_lim_o_lcham) {
            throw new IllegalArgumentException("ATA bo_lim_VALUE_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

