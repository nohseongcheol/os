// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.ذخیرہ_آلہ;

import java.util.Arrays;

/** ATA 28비트 حکم 계층과 같은 512바이트 논리 صیغہ_قدر 장치다. */
public final class 고급기술결합장치 {
    public static final int صیغہ_سائز_دیں = 512;
    private final byte[] کوائف;
    private final boolean فقط_مطالعہ_قدر;

    public 고급기술결합장치(int 구역수, boolean فقط_مطالعہ_قدر) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("صیغہ_قدر 수가 올바르지 않습니다.");
        }
        کوائف = new byte[Math.multiplyExact(구역수, صیغہ_سائز_دیں)];
        this.فقط_مطالعہ_قدر = فقط_مطالعہ_قدر;
    }

    public int 구역수() {
        return کوائف.length / صیغہ_سائز_دیں;
    }

    public void پڑھیں(int صیغہ_اشاریہ, byte[] 받을곳) {
        범위확인(صیغہ_اشاریہ, 받을곳);
        System.arraycopy(کوائف, صیغہ_اشاریہ * صیغہ_سائز_دیں, 받을곳, 0, صیغہ_سائز_دیں);
    }

    public void لکھیں(int صیغہ_اشاریہ, byte[] 쓸자료) {
        if (فقط_مطالعہ_قدر) {
            throw new IllegalStateException("پڑھیں 전용 장치입니다.");
        }
        범위확인(صیغہ_اشاریہ, 쓸자료);
        System.arraycopy(쓸자료, 0, کوائف, صیغہ_اشاریہ * صیغہ_سائز_دیں, صیغہ_سائز_دیں);
    }

    public void 지우기() {
        if (فقط_مطالعہ_قدر) {
            throw new IllegalStateException("پڑھیں 전용 장치입니다.");
        }
        Arrays.fill(کوائف, (byte) 0);
    }

    private void 범위확인(int صیغہ_اشاریہ, byte[] 임시공간) {
        if (صیغہ_اشاریہ < 0 || صیغہ_اشاریہ >= 구역수() || 임시공간.length < صیغہ_سائز_دیں) {
            throw new IllegalArgumentException("ATA صیغہ_قدر 범위가 올바르지 않습니다.");
        }
    }
}

