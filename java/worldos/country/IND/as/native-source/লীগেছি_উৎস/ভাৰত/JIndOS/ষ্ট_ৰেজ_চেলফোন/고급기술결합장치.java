// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.ষ্ট_ৰেজ_চেলফোন;

import java.util.Arrays;

/** ATA 28비트 কমান্ড 계층과 같은 512바이트 논리 শাখা_মান_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int শাখা_আকাৰ_কৰক = 512;
    private final byte[] ডাটা;
    private final boolean ৰিড_অনলি_মান;

    public 고급기술결합장치(int 구역수, boolean ৰিড_অনলি_মান) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("শাখা_মান_366e0bfa 수가 올바르지 않습니다.");
        }
        ডাটা = new byte[Math.multiplyExact(구역수, শাখা_আকাৰ_কৰক)];
        this.ৰিড_অনলি_মান = ৰিড_অনলি_মান;
    }

    public int 구역수() {
        return ডাটা.length / শাখা_আকাৰ_কৰক;
    }

    public void পড়া(int শাখা_ইনডেক্স, byte[] 받을곳) {
        범위확인(শাখা_ইনডেক্স, 받을곳);
        System.arraycopy(ডাটা, শাখা_ইনডেক্স * শাখা_আকাৰ_কৰক, 받을곳, 0, শাখা_আকাৰ_কৰক);
    }

    public void লিখা(int শাখা_ইনডেক্স, byte[] 쓸자료) {
        if (ৰিড_অনলি_মান) {
            throw new IllegalStateException("পড়া 전용 장치입니다.");
        }
        범위확인(শাখা_ইনডেক্স, 쓸자료);
        System.arraycopy(쓸자료, 0, ডাটা, শাখা_ইনডেক্স * শাখা_আকাৰ_কৰক, শাখা_আকাৰ_কৰক);
    }

    public void 지우기() {
        if (ৰিড_অনলি_মান) {
            throw new IllegalStateException("পড়া 전용 장치입니다.");
        }
        Arrays.fill(ডাটা, (byte) 0);
    }

    private void 범위확인(int শাখা_ইনডেক্স, byte[] 임시공간) {
        if (শাখা_ইনডেক্স < 0 || শাখা_ইনডেক্স >= 구역수() || 임시공간.length < শাখা_আকাৰ_কৰক) {
            throw new IllegalArgumentException("ATA শাখা_মান_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

