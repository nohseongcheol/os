// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.Storio_dyfais;

import java.util.Arrays;

/** ATA 28비트 Gorchymyn 계층과 같은 512바이트 논리 adran_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int adran_newid_maint = 512;
    private final byte[] data;
    private final boolean darllen_yn_unig_VALUE;

    public 고급기술결합장치(int adran_COUNT, boolean darllen_yn_unig_VALUE) {
        if (adran_COUNT <= 0) {
            throw new IllegalArgumentException("adran_VALUE 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(adran_COUNT, adran_newid_maint)];
        this.darllen_yn_unig_VALUE = darllen_yn_unig_VALUE;
    }

    public int adran_COUNT() {
        return data.length / adran_newid_maint;
    }

    public void Darllen(int adran_INDEX, byte[] 받을곳) {
        범위확인(adran_INDEX, 받을곳);
        System.arraycopy(data, adran_INDEX * adran_newid_maint, 받을곳, 0, adran_newid_maint);
    }

    public void Ysgrifennu(int adran_INDEX, byte[] 쓸자료) {
        if (darllen_yn_unig_VALUE) {
            throw new IllegalStateException("Darllen 전용 장치입니다.");
        }
        범위확인(adran_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, adran_INDEX * adran_newid_maint, adran_newid_maint);
    }

    public void 지우기() {
        if (darllen_yn_unig_VALUE) {
            throw new IllegalStateException("Darllen 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int adran_INDEX, byte[] 임시공간) {
        if (adran_INDEX < 0 || adran_INDEX >= adran_COUNT() || 임시공간.length < adran_newid_maint) {
            throw new IllegalArgumentException("ATA adran_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

