// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.بوشلۇق_كۆچمە;

import java.util.Arrays;

/** ATA 28비트 بۇيرۇق 계층과 같은 512바이트 논리 بۆلۈم_قىممىتى 장치다. */
public final class 고급기술결합장치 {
    public static final int بۆلۈم_ئۆزگەرتمەك = 512;
    private final byte[] مەلۇمات;
    private final boolean ئوقۇشقىلا_بولىدىغان_قىممىتى;

    public 고급기술결합장치(int 구역수, boolean ئوقۇشقىلا_بولىدىغان_قىممىتى) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("بۆلۈم_قىممىتى 수가 올바르지 않습니다.");
        }
        مەلۇمات = new byte[Math.multiplyExact(구역수, بۆلۈم_ئۆزگەرتمەك)];
        this.ئوقۇشقىلا_بولىدىغان_قىممىتى = ئوقۇشقىلا_بولىدىغان_قىممىتى;
    }

    public int 구역수() {
        return مەلۇمات.length / بۆلۈم_ئۆزگەرتمەك;
    }

    public void ئوقۇ(int بۆلۈم_ئىندېكس, byte[] 받을곳) {
        범위확인(بۆلۈم_ئىندېكس, 받을곳);
        System.arraycopy(مەلۇمات, بۆلۈم_ئىندېكس * بۆلۈم_ئۆزگەرتمەك, 받을곳, 0, بۆلۈم_ئۆزگەرتمەك);
    }

    public void ياز(int بۆلۈم_ئىندېكس, byte[] 쓸자료) {
        if (ئوقۇشقىلا_بولىدىغان_قىممىتى) {
            throw new IllegalStateException("ئوقۇ 전용 장치입니다.");
        }
        범위확인(بۆلۈم_ئىندېكس, 쓸자료);
        System.arraycopy(쓸자료, 0, مەلۇمات, بۆلۈم_ئىندېكس * بۆلۈم_ئۆزگەرتمەك, بۆلۈم_ئۆزگەرتمەك);
    }

    public void 지우기() {
        if (ئوقۇشقىلا_بولىدىغان_قىممىتى) {
            throw new IllegalStateException("ئوقۇ 전용 장치입니다.");
        }
        Arrays.fill(مەلۇمات, (byte) 0);
    }

    private void 범위확인(int بۆلۈم_ئىندېكس, byte[] 임시공간) {
        if (بۆلۈم_ئىندېكس < 0 || بۆلۈم_ئىندېكس >= 구역수() || 임시공간.length < بۆلۈم_ئۆزگەرتمەك) {
            throw new IllegalArgumentException("ATA بۆلۈم_قىممىتى 범위가 올바르지 않습니다.");
        }
    }
}

