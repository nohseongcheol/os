// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.ذخیرہ_آلہ;

import java.util.Arrays;

/** ATA 28비트 حکم 계층과 같은 512바이트 논리 سیکشن_قدر 장치다. */
public final class 고급기술결합장치 {
    public static final int سیکشن_سائز = 512;
    private final byte[] کوائف;
    private final boolean صرف_مطالعہ_قدر;

    public 고급기술결합장치(int 구역수, boolean صرف_مطالعہ_قدر) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("سیکشن_قدر 수가 올바르지 않습니다.");
        }
        کوائف = new byte[Math.multiplyExact(구역수, سیکشن_سائز)];
        this.صرف_مطالعہ_قدر = صرف_مطالعہ_قدر;
    }

    public int 구역수() {
        return کوائف.length / سیکشن_سائز;
    }

    public void 읽기(int سیکشن_اشاریہ, byte[] 받을곳) {
        범위확인(سیکشن_اشاریہ, 받을곳);
        System.arraycopy(کوائف, سیکشن_اشاریہ * سیکشن_سائز, 받을곳, 0, سیکشن_سائز);
    }

    public void لکھو(int سیکشن_اشاریہ, byte[] 쓸자료) {
        if (صرف_مطالعہ_قدر) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(سیکشن_اشاریہ, 쓸자료);
        System.arraycopy(쓸자료, 0, کوائف, سیکشن_اشاریہ * سیکشن_سائز, سیکشن_سائز);
    }

    public void 지우기() {
        if (صرف_مطالعہ_قدر) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(کوائف, (byte) 0);
    }

    private void 범위확인(int سیکشن_اشاریہ, byte[] 임시공간) {
        if (سیکشن_اشاریہ < 0 || سیکشن_اشاریہ >= 구역수() || 임시공간.length < سیکشن_سائز) {
            throw new IllegalArgumentException("ATA سیکشن_قدر 범위가 올바르지 않습니다.");
        }
    }
}

