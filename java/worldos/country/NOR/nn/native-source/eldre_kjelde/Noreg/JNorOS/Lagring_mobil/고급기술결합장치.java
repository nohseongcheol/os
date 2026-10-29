// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.Lagring_mobil;

import java.util.Arrays;

/** ATA 28비트 Kommando 계층과 같은 512바이트 논리 del_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int del_endre_storleik = 512;
    private final byte[] data;
    private final boolean skriveverna_VALUE;

    public 고급기술결합장치(int del_COUNT, boolean skriveverna_VALUE) {
        if (del_COUNT <= 0) {
            throw new IllegalArgumentException("del_VALUE 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(del_COUNT, del_endre_storleik)];
        this.skriveverna_VALUE = skriveverna_VALUE;
    }

    public int del_COUNT() {
        return data.length / del_endre_storleik;
    }

    public void Les(int del_INDEX, byte[] 받을곳) {
        범위확인(del_INDEX, 받을곳);
        System.arraycopy(data, del_INDEX * del_endre_storleik, 받을곳, 0, del_endre_storleik);
    }

    public void Skriv(int del_INDEX, byte[] 쓸자료) {
        if (skriveverna_VALUE) {
            throw new IllegalStateException("Les 전용 장치입니다.");
        }
        범위확인(del_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, del_INDEX * del_endre_storleik, del_endre_storleik);
    }

    public void 지우기() {
        if (skriveverna_VALUE) {
            throw new IllegalStateException("Les 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int del_INDEX, byte[] 임시공간) {
        if (del_INDEX < 0 || del_INDEX >= del_COUNT() || 임시공간.length < del_endre_storleik) {
            throw new IllegalArgumentException("ATA del_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

