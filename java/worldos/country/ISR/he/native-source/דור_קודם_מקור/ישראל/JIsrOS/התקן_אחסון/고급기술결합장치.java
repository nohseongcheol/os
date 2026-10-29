// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.התקן_אחסון;

import java.util.Arrays;

/** ATA 28비트 פקודה 계층과 같은 512바이트 논리 מקטע_ערך 장치다. */
public final class 고급기술결합장치 {
    public static final int מקטע_גודל = 512;
    private final byte[] נתונים;
    private final boolean לקריאה_בלבד_ערך;

    public 고급기술결합장치(int 구역수, boolean לקריאה_בלבד_ערך) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("מקטע_ערך 수가 올바르지 않습니다.");
        }
        נתונים = new byte[Math.multiplyExact(구역수, מקטע_גודל)];
        this.לקריאה_בלבד_ערך = לקריאה_בלבד_ערך;
    }

    public int 구역수() {
        return נתונים.length / מקטע_גודל;
    }

    public void קרא(int מקטע_מדד, byte[] לקבל_יעד) {
        שיק_טווח(מקטע_מדד, לקבל_יעד);
        System.arraycopy(נתונים, מקטע_מדד * מקטע_גודל, לקבל_יעד, 0, מקטע_גודל);
    }

    public void כתוב(int מקטע_מדד, byte[] 쓸자료) {
        if (לקריאה_בלבד_ערך) {
            throw new IllegalStateException("קרא 전용 장치입니다.");
        }
        שיק_טווח(מקטע_מדד, 쓸자료);
        System.arraycopy(쓸자료, 0, נתונים, מקטע_מדד * מקטע_גודל, מקטע_גודל);
    }

    public void מחק_ערך() {
        if (לקריאה_בלבד_ערך) {
            throw new IllegalStateException("קרא 전용 장치입니다.");
        }
        Arrays.fill(נתונים, (byte) 0);
    }

    private void שיק_טווח(int מקטע_מדד, byte[] 임시공간) {
        if (מקטע_מדד < 0 || מקטע_מדד >= 구역수() || 임시공간.length < מקטע_גודל) {
            throw new IllegalArgumentException("ATA מקטע_ערך 범위가 올바르지 않습니다.");
        }
    }
}

