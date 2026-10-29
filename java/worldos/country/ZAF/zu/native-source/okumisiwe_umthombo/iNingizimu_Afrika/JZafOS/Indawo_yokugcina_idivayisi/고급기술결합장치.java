// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iNingizimu_Afrika.JZafOS.Indawo_yokugcina_idivayisi;

import java.util.Arrays;

/** ATA 28비트 Umlayelo 계층과 같은 512바이트 논리 isigaba_inani 장치다. */
public final class 고급기술결합장치 {
    public static final int isigaba_linganisa = 512;
    private final byte[] imininingwane;
    private final boolean fundwayo_kuphela_inani;

    public 고급기술결합장치(int 구역수, boolean fundwayo_kuphela_inani) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("isigaba_inani 수가 올바르지 않습니다.");
        }
        imininingwane = new byte[Math.multiplyExact(구역수, isigaba_linganisa)];
        this.fundwayo_kuphela_inani = fundwayo_kuphela_inani;
    }

    public int 구역수() {
        return imininingwane.length / isigaba_linganisa;
    }

    public void Funda(int isigaba_thola_inkomba, byte[] 받을곳) {
        범위확인(isigaba_thola_inkomba, 받을곳);
        System.arraycopy(imininingwane, isigaba_thola_inkomba * isigaba_linganisa, 받을곳, 0, isigaba_linganisa);
    }

    public void Bhala(int isigaba_thola_inkomba, byte[] 쓸자료) {
        if (fundwayo_kuphela_inani) {
            throw new IllegalStateException("Funda 전용 장치입니다.");
        }
        범위확인(isigaba_thola_inkomba, 쓸자료);
        System.arraycopy(쓸자료, 0, imininingwane, isigaba_thola_inkomba * isigaba_linganisa, isigaba_linganisa);
    }

    public void 지우기() {
        if (fundwayo_kuphela_inani) {
            throw new IllegalStateException("Funda 전용 장치입니다.");
        }
        Arrays.fill(imininingwane, (byte) 0);
    }

    private void 범위확인(int isigaba_thola_inkomba, byte[] 임시공간) {
        if (isigaba_thola_inkomba < 0 || isigaba_thola_inkomba >= 구역수() || 임시공간.length < isigaba_linganisa) {
            throw new IllegalArgumentException("ATA isigaba_inani 범위가 올바르지 않습니다.");
        }
    }
}

