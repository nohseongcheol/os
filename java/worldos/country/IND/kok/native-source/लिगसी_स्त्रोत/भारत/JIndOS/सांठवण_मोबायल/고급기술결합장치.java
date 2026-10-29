// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.सांठवण_मोबायल;

import java.util.Arrays;

/** ATA 28비트 आदेश 계층과 같은 512바이트 논리 विभाग_मोल 장치다. */
public final class 고급기술결합장치 {
    public static final int विभाग_आवाठ = 512;
    private final byte[] डेटा;
    private final boolean फकत_वाचचें_मोल;

    public 고급기술결합장치(int विभाग_COUNT, boolean फकत_वाचचें_मोल) {
        if (विभाग_COUNT <= 0) {
            throw new IllegalArgumentException("विभाग_मोल 수가 올바르지 않습니다.");
        }
        डेटा = new byte[Math.multiplyExact(विभाग_COUNT, विभाग_आवाठ)];
        this.फकत_वाचचें_मोल = फकत_वाचचें_मोल;
    }

    public int विभाग_COUNT() {
        return डेटा.length / विभाग_आवाठ;
    }

    public void 읽기(int विभाग_INDEX, byte[] 받을곳) {
        범위확인(विभाग_INDEX, 받을곳);
        System.arraycopy(डेटा, विभाग_INDEX * विभाग_आवाठ, 받을곳, 0, विभाग_आवाठ);
    }

    public void बरोवचें(int विभाग_INDEX, byte[] 쓸자료) {
        if (फकत_वाचचें_मोल) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(विभाग_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, डेटा, विभाग_INDEX * विभाग_आवाठ, विभाग_आवाठ);
    }

    public void 지우기() {
        if (फकत_वाचचें_मोल) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(डेटा, (byte) 0);
    }

    private void 범위확인(int विभाग_INDEX, byte[] 임시공간) {
        if (विभाग_INDEX < 0 || विभाग_INDEX >= विभाग_COUNT() || 임시공간.length < विभाग_आवाठ) {
            throw new IllegalArgumentException("ATA विभाग_मोल 범위가 올바르지 않습니다.");
        }
    }
}

