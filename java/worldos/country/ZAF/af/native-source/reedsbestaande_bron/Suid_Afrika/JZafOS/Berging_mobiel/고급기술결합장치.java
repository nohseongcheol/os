// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.Berging_mobiel;

import java.util.Arrays;

/** ATA 28비트 Opdrag 계층과 같은 512바이트 논리 seksie_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int seksie_verstel = 512;
    private final byte[] data;
    private final boolean leesalleen_VALUE;

    public 고급기술결합장치(int seksie_COUNT, boolean leesalleen_VALUE) {
        if (seksie_COUNT <= 0) {
            throw new IllegalArgumentException("seksie_VALUE 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(seksie_COUNT, seksie_verstel)];
        this.leesalleen_VALUE = leesalleen_VALUE;
    }

    public int seksie_COUNT() {
        return data.length / seksie_verstel;
    }

    public void Lees(int seksie_INDEX, byte[] 받을곳) {
        범위확인(seksie_INDEX, 받을곳);
        System.arraycopy(data, seksie_INDEX * seksie_verstel, 받을곳, 0, seksie_verstel);
    }

    public void Skryf(int seksie_INDEX, byte[] 쓸자료) {
        if (leesalleen_VALUE) {
            throw new IllegalStateException("Lees 전용 장치입니다.");
        }
        범위확인(seksie_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, seksie_INDEX * seksie_verstel, seksie_verstel);
    }

    public void vee_uit_inskrywing() {
        if (leesalleen_VALUE) {
            throw new IllegalStateException("Lees 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int seksie_INDEX, byte[] 임시공간) {
        if (seksie_INDEX < 0 || seksie_INDEX >= seksie_COUNT() || 임시공간.length < seksie_verstel) {
            throw new IllegalArgumentException("ATA seksie_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

