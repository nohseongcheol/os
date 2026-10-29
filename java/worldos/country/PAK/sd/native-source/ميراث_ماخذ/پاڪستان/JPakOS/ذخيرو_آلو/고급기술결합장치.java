// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.ذخيرو_آلو;

import java.util.Arrays;

/** ATA 28비트 حڪم 계층과 같은 512바이트 논리 سيڪشن_قدر 장치다. */
public final class 고급기술결합장치 {
    public static final int سيڪشن_سائيز = 512;
    private final byte[] ڪوائف;
    private final boolean صرف_مطالعو_قدر;

    public 고급기술결합장치(int 구역수, boolean صرف_مطالعو_قدر) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("سيڪشن_قدر 수가 올바르지 않습니다.");
        }
        ڪوائف = new byte[Math.multiplyExact(구역수, سيڪشن_سائيز)];
        this.صرف_مطالعو_قدر = صرف_مطالعو_قدر;
    }

    public int 구역수() {
        return ڪوائف.length / سيڪشن_سائيز;
    }

    public void 읽기(int سيڪشن_ابتدائي, byte[] 받을곳) {
        범위확인(سيڪشن_ابتدائي, 받을곳);
        System.arraycopy(ڪوائف, سيڪشن_ابتدائي * سيڪشن_سائيز, 받을곳, 0, سيڪشن_سائيز);
    }

    public void لکو(int سيڪشن_ابتدائي, byte[] 쓸자료) {
        if (صرف_مطالعو_قدر) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(سيڪشن_ابتدائي, 쓸자료);
        System.arraycopy(쓸자료, 0, ڪوائف, سيڪشن_ابتدائي * سيڪشن_سائيز, سيڪشن_سائيز);
    }

    public void 지우기() {
        if (صرف_مطالعو_قدر) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(ڪوائف, (byte) 0);
    }

    private void 범위확인(int سيڪشن_ابتدائي, byte[] 임시공간) {
        if (سيڪشن_ابتدائي < 0 || سيڪشن_ابتدائي >= 구역수() || 임시공간.length < سيڪشن_سائيز) {
            throw new IllegalArgumentException("ATA سيڪشن_قدر 범위가 올바르지 않습니다.");
        }
    }
}

