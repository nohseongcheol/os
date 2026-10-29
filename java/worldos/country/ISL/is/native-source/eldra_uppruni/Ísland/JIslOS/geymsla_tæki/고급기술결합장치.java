// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.geymsla_tæki;

import java.util.Arrays;

/** ATA 28비트 Skipun 계층과 같은 512바이트 논리 hluti_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int hluti_breyta_stærð = 512;
    private final byte[] gögn;
    private final boolean skrifvarið_VALUE;

    public 고급기술결합장치(int hluti_COUNT, boolean skrifvarið_VALUE) {
        if (hluti_COUNT <= 0) {
            throw new IllegalArgumentException("hluti_VALUE 수가 올바르지 않습니다.");
        }
        gögn = new byte[Math.multiplyExact(hluti_COUNT, hluti_breyta_stærð)];
        this.skrifvarið_VALUE = skrifvarið_VALUE;
    }

    public int hluti_COUNT() {
        return gögn.length / hluti_breyta_stærð;
    }

    public void Lestur(int hluti_INDEX, byte[] 받을곳) {
        범위확인(hluti_INDEX, 받을곳);
        System.arraycopy(gögn, hluti_INDEX * hluti_breyta_stærð, 받을곳, 0, hluti_breyta_stærð);
    }

    public void Skrift(int hluti_INDEX, byte[] 쓸자료) {
        if (skrifvarið_VALUE) {
            throw new IllegalStateException("Lestur 전용 장치입니다.");
        }
        범위확인(hluti_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, gögn, hluti_INDEX * hluti_breyta_stærð, hluti_breyta_stærð);
    }

    public void eyða_færsla() {
        if (skrifvarið_VALUE) {
            throw new IllegalStateException("Lestur 전용 장치입니다.");
        }
        Arrays.fill(gögn, (byte) 0);
    }

    private void 범위확인(int hluti_INDEX, byte[] 임시공간) {
        if (hluti_INDEX < 0 || hluti_INDEX >= hluti_COUNT() || 임시공간.length < hluti_breyta_stærð) {
            throw new IllegalArgumentException("ATA hluti_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

